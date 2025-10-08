#!/usr/bin/env python3
"""
Easy Featured Projects Manager
Just edit the FEATURED list below and run: python3 update_featured.py
"""

import re
import subprocess

# ========================================
# EDIT THIS LIST TO CHANGE FEATURED PROJECTS
# ========================================
FEATURED = [
    "NVIDIA AI Report Generator",
    "Finexa",
    "RAG Mastery Hub",
    "SEO Analyzer Pro",
]

# ========================================
# You can also mark projects as locked (in development)
# ========================================
LOCKED = [
    "Elder Guardian",
    "Mars Mission Isaac",
]

# ========================================
# Script starts here - no need to edit below
# ========================================

def update_featured_projects():
    print("🔧 Updating featured projects...\n")

    # Read the file
    with open('index.html', 'r') as f:
        content = f.read()

    # Find the projects section
    projects_start = content.find('<!-- Featured Projects -->')
    projects_end = content.find('<!-- Private Projects Section -->')

    before_projects = content[:projects_start]
    after_projects = content[projects_end:]
    projects_section = content[projects_start:projects_end]

    # Extract individual projects
    projects = re.findall(r'(\n\n        <!-- .*?(?:</a>|</div>))', projects_section, re.DOTALL)

    # Process each project
    featured_projects = []
    locked_projects = []
    regular_projects = []

    for project in projects:
        # Get project name from comment
        name_match = re.search(r'<!-- (.*?) -->', project)
        if not name_match:
            continue
        name = name_match.group(1)

        # Remove any existing featured/locked classes
        project = re.sub(r' class="project-card featured"', ' class="project-card"', project)
        project = re.sub(r' class="project-card locked"', ' class="project-card"', project)
        project = re.sub(r'<span class="featured-badge">⭐ Featured</span>\s*', '', project)
        project = re.sub(r'<span class="lock-badge">🔒 In Development</span>\s*', '', project)
        project = re.sub(r'<h3>🔒 ', '<h3>👴 ' if 'Elder' in name else '<h3>🚀 ', project)

        # Categorize and modify based on lists
        if name in FEATURED:
            # Make it featured
            project = project.replace(' class="project-card"', ' class="project-card featured"')
            project = project.replace('<div class="project-card featured">', '<a href="https://github.com/KlementMultiverse/' + name.lower().replace(' ', '-') + '" target="_blank" class="project-card featured">')
            project = project.replace('</div>', '</a>')
            # Add featured badge
            project = project.replace('<span class="featured-badge">⭐ Featured</span>', '')
            project = project.replace('<div class="project-header">', '<span class="featured-badge">⭐ Featured</span>\n          <div class="project-header">')
            featured_projects.append(project)
            print(f"✅ Featured: {name}")

        elif name in LOCKED:
            # Make it locked
            project = project.replace('<a href=', '<div class="project-card locked">\n          <div class="project-header">\n            <h3>🔒')
            project = re.sub(r' class="project-card"', ' class="project-card locked"', project)
            project = re.sub(r'<a href="[^"]*" target="_blank" class="project-card[^"]*">', '<div class="project-card locked">', project)
            project = project.replace('</a>', '</div>')
            project = re.sub(r'<h3>[^🔒]*', '<h3>🔒 ', project)
            # Add lock badge
            project = project.replace('<span class="lock-badge">🔒 In Development</span>', '')
            if '<h3>🔒' in project:
                project = re.sub(r'(<h3>🔒 [^<]+</h3>)', r'\1\n            <span class="lock-badge">🔒 In Development</span>', project)
            locked_projects.append(project)
            print(f"🔒 Locked: {name}")

        else:
            # Regular project
            regular_projects.append(project)
            print(f"📁 Regular: {name}")

    # Reconstruct
    header = '''<!-- Featured Projects -->
      <h2>Featured Projects</h2>
      <div class="projects-grid">'''

    new_projects_section = (
        header +
        ''.join(featured_projects) +
        ''.join(locked_projects) +
        ''.join(regular_projects) +
        '\n      </div>\n\n      '
    )

    # Write back
    new_content = before_projects + new_projects_section + after_projects

    with open('index.html', 'w') as f:
        f.write(new_content)

    print(f"\n✅ Updated! {len(featured_projects)} featured, {len(locked_projects)} locked, {len(regular_projects)} regular")

    # Git commit and push
    print("\n📤 Pushing to GitHub...")
    subprocess.run(['git', 'add', 'index.html'], check=True)
    subprocess.run([
        'git', 'commit', '-m',
        f'Update featured projects: {", ".join(FEATURED)}\n\n🤖 Generated with update_featured.py'
    ], check=True)
    subprocess.run(['git', 'push', 'origin', 'main'], check=True)

    print("\n🎉 Done! Check https://klementmultiverse.github.io/")

if __name__ == '__main__':
    update_featured_projects()
