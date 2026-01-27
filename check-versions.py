#!/usr/bin/env python3
"""
Check for Atlassian product updates.
Dynamically discovers LTS versions from Atlassian release notes.
Tracks LTS versions for Jira, Confluence, Bitbucket, Bamboo.
Tracks latest version for Crowd.

Usage:
  python3 check-versions.py          # Check only
  python3 check-versions.py --update # Check and apply updates
"""

import argparse
import json
import re
import shutil
import sys
from pathlib import Path
from typing import Optional
import urllib.request
import urllib.error

# Product configuration
PRODUCTS = {
    "jira": {
        "docker_image": "atlassian/jira-software",
        "lts": True,
        "release_notes_pattern": "https://confluence.atlassian.com/display/JIRASOFTWARE/JIRA+Software+{version}.x+release+notes",
    },
    "confluence": {
        "docker_image": "atlassian/confluence",
        "lts": True,
        "release_notes_pattern": "https://confluence.atlassian.com/display/DOC/Confluence+{version}+Release+Notes",
    },
    "bitbucket": {
        "docker_image": "atlassian/bitbucket",
        "lts": True,
        "release_notes_pattern": "https://confluence.atlassian.com/display/BitbucketServer/Bitbucket+Data+Center+{version}+release+notes",
    },
    "bamboo": {
        "docker_image": "atlassian/bamboo",
        "lts": True,
        "release_notes_pattern": "https://confluence.atlassian.com/display/BAMBOORELEASES/Bamboo+{version}+release+notes",
    },
    "crowd": {
        "docker_image": "atlassian/crowd",
        "lts": False,
    },
}

REPO_ROOT = Path(__file__).parent

# Cache for LTS check results
_lts_cache: dict[str, bool] = {}


def fetch_url(url: str, timeout: int = 15) -> Optional[str]:
    """Fetch URL content, return None on error."""
    try:
        req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
        with urllib.request.urlopen(req, timeout=timeout) as resp:
            return resp.read().decode("utf-8", errors="ignore")
    except Exception:
        return None


def is_lts_version(product: str, branch: str, config: dict) -> bool:
    """Check if a version branch is LTS by checking release notes."""
    cache_key = f"{product}:{branch}"
    if cache_key in _lts_cache:
        return _lts_cache[cache_key]
    
    pattern = config.get("release_notes_pattern")
    if not pattern:
        return False
    
    url = pattern.format(version=branch)
    content = fetch_url(url)
    
    if content is None:
        _lts_cache[cache_key] = False
        return False
    
    # Check for LTS indicators in the page
    is_lts = any(phrase in content.lower() for phrase in [
        "long term support",
        "long-term support",
        "lts release",
        "is a lts",
    ])
    
    _lts_cache[cache_key] = is_lts
    return is_lts


def get_docker_tags(image: str, max_pages: int = 5) -> list[str]:
    """Fetch tags from Docker Hub API with pagination."""
    all_tags = []
    url = f"https://hub.docker.com/v2/repositories/{image}/tags?page_size=100&ordering=last_updated"
    
    for _ in range(max_pages):
        try:
            with urllib.request.urlopen(url, timeout=30) as resp:
                data = json.loads(resp.read().decode())
                tags = [tag["name"] for tag in data.get("results", [])]
                all_tags.extend(tags)
                next_url = data.get("next")
                if not next_url:
                    break
                url = next_url
        except urllib.error.URLError:
            break
    
    return all_tags


def parse_version(tag: str) -> Optional[tuple[int, int, int]]:
    """Parse version string to tuple. Handles X.Y.Z and X.Y.Z-suffix formats."""
    match = re.match(r"^(\d+)\.(\d+)\.(\d+)(?:-|$)", tag)
    if match:
        return (int(match.group(1)), int(match.group(2)), int(match.group(3)))
    return None


def get_version_branch(version: str) -> Optional[str]:
    """Get major.minor branch from version string."""
    parsed = parse_version(version)
    if parsed:
        return f"{parsed[0]}.{parsed[1]}"
    return None


def get_current_version(product: str) -> Optional[str]:
    """Extract current version from Dockerfile."""
    dockerfile = REPO_ROOT / product / "Dockerfile"
    if not dockerfile.exists():
        return None
    
    content = dockerfile.read_text()
    match = re.search(r"FROM\s+\S+:(\d+\.\d+\.\d+)", content)
    if match:
        return match.group(1)
    return None


def filter_clean_versions(tags: list[str]) -> list[tuple[tuple[int, int, int], str]]:
    """Filter tags to clean X.Y.Z versions (no suffixes) and parse them."""
    versions = []
    for tag in tags:
        if re.match(r"^\d+\.\d+\.\d+$", tag):
            parsed = parse_version(tag)
            if parsed:
                versions.append((parsed, tag))
    return versions


def get_unique_branches(versions: list[tuple[tuple[int, int, int], str]]) -> list[str]:
    """Get unique major.minor branches from versions, sorted descending."""
    branches = set()
    for parsed, _ in versions:
        branches.add(f"{parsed[0]}.{parsed[1]}")
    return sorted(branches, key=lambda b: tuple(map(int, b.split("."))), reverse=True)


def get_latest_in_branch(versions: list[tuple[tuple[int, int, int], str]], branch: str) -> Optional[str]:
    """Get latest version within a specific major.minor branch."""
    branch_parts = tuple(map(int, branch.split(".")))
    branch_versions = [(p, t) for p, t in versions if (p[0], p[1]) == branch_parts]
    
    if not branch_versions:
        return None
    
    branch_versions.sort(key=lambda x: x[0], reverse=True)
    return branch_versions[0][1]


def find_latest_lts(product: str, config: dict, versions: list[tuple[tuple[int, int, int], str]]) -> tuple[Optional[str], Optional[str]]:
    """Find the latest LTS version by checking release notes. Returns (version, branch)."""
    branches = get_unique_branches(versions)
    
    # Check branches from newest to oldest
    checked = 0
    for branch in branches:
        # Limit how many branches we check to avoid too many HTTP requests
        if checked >= 5:
            break
        
        print(f"    Checking {branch}...", end=" ", flush=True)
        if is_lts_version(product, branch, config):
            print("LTS ✓")
            latest = get_latest_in_branch(versions, branch)
            return (latest, branch)
        else:
            print("not LTS")
        checked += 1
    
    return (None, None)


def get_latest_version(versions: list[tuple[tuple[int, int, int], str]]) -> Optional[str]:
    """Get absolute latest version."""
    if not versions:
        return None
    versions_sorted = sorted(versions, key=lambda x: x[0], reverse=True)
    return versions_sorted[0][1]


def update_dockerfile(product: str, old_version: str, new_version: str) -> bool:
    """Update the version in a Dockerfile."""
    dockerfile = REPO_ROOT / product / "Dockerfile"
    if not dockerfile.exists():
        return False
    
    content = dockerfile.read_text()
    new_content = content.replace(f":{old_version}", f":{new_version}")
    
    if content == new_content:
        print(f"  ⚠️  No changes made to Dockerfile")
        return False
    
    dockerfile.write_text(new_content)
    return True


def archive_old_version(product: str, old_branch: str) -> bool:
    """Archive the current Dockerfile to a versioned subdirectory."""
    product_dir = REPO_ROOT / product
    archive_dir = product_dir / old_branch
    dockerfile = product_dir / "Dockerfile"
    
    if not dockerfile.exists():
        return False
    
    # Create archive directory if it doesn't exist
    archive_dir.mkdir(exist_ok=True)
    
    # Copy Dockerfile to archive
    archived_dockerfile = archive_dir / "Dockerfile"
    shutil.copy2(dockerfile, archived_dockerfile)
    
    print(f"  📁 Archived to {product}/{old_branch}/Dockerfile")
    return True


def apply_update(result: dict, config: dict) -> bool:
    """Apply an update based on the check result."""
    product = result["product"]
    current = result["current"]
    latest = result["latest"]
    current_branch = result["current_branch"]
    latest_branch = result["latest_branch"]
    major_minor_change = result["major_minor_change"]
    
    print(f"\n🔧 Updating {product.upper()}: {current} → {latest}")
    
    # If major.minor changed, archive old version first
    if major_minor_change:
        print(f"  Major.minor change detected: {current_branch} → {latest_branch}")
        if not archive_old_version(product, current_branch):
            print(f"  ❌ Failed to archive old version")
            return False
    
    # Update the Dockerfile
    if update_dockerfile(product, current, latest):
        print(f"  ✅ Updated Dockerfile: {current} → {latest}")
        return True
    else:
        print(f"  ❌ Failed to update Dockerfile")
        return False


def check_product(product: str, config: dict) -> dict:
    """Check a single product for updates."""
    result = {
        "product": product,
        "current": None,
        "latest": None,
        "current_branch": None,
        "latest_branch": None,
        "needs_update": False,
        "major_minor_change": False,
        "docker_image": config["docker_image"],
    }
    
    print(f"\n📦 {product.upper()}")
    
    # Get current version
    current = get_current_version(product)
    if not current:
        print(f"  ⚠️  No Dockerfile found or version not detected")
        return result
    
    result["current"] = current
    result["current_branch"] = get_version_branch(current)
    print(f"  Current: {current} (branch: {result['current_branch']})")
    
    # Fetch Docker Hub tags
    print(f"  Fetching tags from Docker Hub...", end=" ", flush=True)
    tags = get_docker_tags(config["docker_image"])
    versions = filter_clean_versions(tags)
    print(f"found {len(versions)} versions")
    
    if not versions:
        print(f"  ⚠️  No valid versions found")
        return result
    
    # Get latest version
    if config["lts"]:
        print(f"  Discovering LTS branches...")
        latest, latest_branch = find_latest_lts(product, config, versions)
        result["latest_branch"] = latest_branch
        if latest:
            print(f"  Latest LTS: {latest} (branch: {latest_branch})")
        else:
            print(f"  ⚠️  No LTS version found")
    else:
        latest = get_latest_version(versions)
        if latest:
            result["latest_branch"] = get_version_branch(latest)
            print(f"  Latest: {latest}")
    
    result["latest"] = latest
    
    # Compare versions
    if latest and current:
        current_parsed = parse_version(current)
        latest_parsed = parse_version(latest)
        
        if latest_parsed and current_parsed:
            if latest_parsed > current_parsed:
                result["needs_update"] = True
                if (latest_parsed[0], latest_parsed[1]) != (current_parsed[0], current_parsed[1]):
                    result["major_minor_change"] = True
                    print(f"  🔄 Major update: {current} → {latest}")
                else:
                    print(f"  📝 Patch update: {current} → {latest}")
            else:
                print(f"  ✅ Up to date")
    
    return result


def main():
    parser = argparse.ArgumentParser(description="Check and update Atlassian Docker images")
    parser.add_argument("--update", action="store_true", help="Apply available updates")
    parser.add_argument("--product", type=str, help="Only check/update specific product")
    args = parser.parse_args()
    
    print("=" * 60)
    if args.update:
        print("Atlassian Version Checker & Updater")
    else:
        print("Atlassian Version Checker (with LTS auto-discovery)")
    print("=" * 60)
    
    # Filter products if --product specified
    products_to_check = PRODUCTS
    if args.product:
        if args.product not in PRODUCTS:
            print(f"Unknown product: {args.product}")
            print(f"Available: {', '.join(PRODUCTS.keys())}")
            return 1
        products_to_check = {args.product: PRODUCTS[args.product]}
    
    results = []
    for product, config in products_to_check.items():
        result = check_product(product, config)
        results.append(result)
    
    # Summary
    print("\n" + "=" * 60)
    print("SUMMARY")
    print("=" * 60)
    
    updates_needed = [r for r in results if r["needs_update"]]
    if not updates_needed:
        print("\n✅ All products are up to date!")
        return 0
    
    print(f"\n📋 {len(updates_needed)} update(s) available:\n")
    for r in updates_needed:
        marker = "🔄 MAJOR" if r["major_minor_change"] else "📝 patch"
        print(f"  {marker} {r['product']}: {r['current']} → {r['latest']}")
        if r["major_minor_change"]:
            print(f"         └─ Archive {r['current_branch']}/, update to {r['latest_branch']}")
    
    # Apply updates if --update flag
    if args.update:
        print("\n" + "=" * 60)
        print("APPLYING UPDATES")
        print("=" * 60)
        
        success_count = 0
        for r in updates_needed:
            config = PRODUCTS[r["product"]]
            if apply_update(r, config):
                success_count += 1
        
        print("\n" + "=" * 60)
        print(f"✅ Applied {success_count}/{len(updates_needed)} update(s)")
        print("=" * 60)
        
        if success_count < len(updates_needed):
            return 1
    else:
        print("\nRun with --update to apply these updates.")
    
    print()
    return 0 if not updates_needed or args.update else 1


if __name__ == "__main__":
    sys.exit(main())
