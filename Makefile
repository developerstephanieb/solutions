# ==============================================================================
# REF-SERIES AUTOMATION (ref-dsa)
# ==============================================================================

# 1. SETUP
# Creates the standard directory structure for a new Ref-Series repo.
# Run this immediately after cloning/creating the repo.
init: assets
	@echo "Initializing Ref-Series structure..."
	@mkdir -p _drafts
	@mkdir -p _scratch
	@mkdir -p _templates
	@mkdir -p 99-resources/assets
	@mkdir -p 99-resources/scripts
	@touch _scratch/.gitkeep
	@echo "- [ ] " > _drafts/TODO.md
	@echo "Done. Directory structure created."

# 2. ASSETS
# Generates the local SVG badges (Easy/Medium/Hard/Unknown) required by the index script.
# Ensures that difficulty labels in generated markdown files work offline.
assets:
	@echo "Generating Badge Assets..."
	@mkdir -p 99-resources/assets
	@echo '<svg xmlns="http://www.w3.org/2000/svg" width="44" height="20"><rect width="44" height="20" fill="#108548" rx="2" ry="2"/><text x="22" y="14" font-family="Verdana,sans-serif" font-size="11" fill="#fff" text-anchor="middle">Easy</text></svg>' > 99-resources/assets/badge-easy.svg
	@echo '<svg xmlns="http://www.w3.org/2000/svg" width="60" height="20"><rect width="60" height="20" fill="#b65c00" rx="2" ry="2"/><text x="30" y="14" font-family="Verdana,sans-serif" font-size="11" fill="#fff" text-anchor="middle">Medium</text></svg>' > 99-resources/assets/badge-medium.svg
	@echo '<svg xmlns="http://www.w3.org/2000/svg" width="44" height="20"><rect width="44" height="20" fill="#C53030" rx="2" ry="2"/><text x="22" y="14" font-family="Verdana,sans-serif" font-size="11" fill="#fff" text-anchor="middle">Hard</text></svg>' > 99-resources/assets/badge-hard.svg
	@echo '<svg xmlns="http://www.w3.org/2000/svg" width="62" height="20"><rect width="62" height="20" fill="#555" rx="2" ry="2"/><text x="31" y="14" font-family="Verdana,sans-serif" font-size="11" fill="#fff" text-anchor="middle">Unknown</text></svg>' > 99-resources/assets/badge-unknown.svg
	@echo "Assets created."

# 3. CLEANUP
# Wipes the contents of the _scratch directory but keeps the folder.
# Useful for resetting your workspace after testing snippets.
clean-scratch:
	@echo "Cleaning _scratch directory..."
	@rm -rf _scratch/*
	@touch _scratch/.gitkeep
	@echo "Scratchpad cleared."

# 4. AUDIT
# Count the number of units, modules, and solutions.
stats:
	@echo "Project Statistics:"
	@echo "Units: $$(find . -maxdepth 1 -type d -name '[0-9]*' | wc -l | xargs)"
	@echo "Modules: $$(find . -name '[0-9]*.md' | wc -l | xargs)"
	@echo "Solutions: $$(find 98-solutions -name '*.py' | wc -l | xargs)"

# 5. AUTOMATION
# Generates the Topic and Company index files in 99-resources.
# Requires python3 and the generate_indexes.py script.
index:
	@echo "Updating Indices..."
	@cd 99-resources/scripts && python3 generate_indexes.py
	@echo "Indices updated successfully."

# 6. HELP
# Lists available commands.
help:
	@echo "Available commands:"
	@echo "  make init          - Create standard directory structure"
	@echo "  make assets        - Generate SVG badges for offline documentation"
	@echo "  make clean-scratch - Delete all files in _scratch/"
	@echo "  make stats         - Show count of Units, Modules, and Solutions"
	@echo "  make index         - Generate Topic and Company index files"