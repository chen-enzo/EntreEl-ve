help:
	@echo
	@echo
	@echo "make receuil <-- convertit le .md en pdf"
	@echo
	@echo

VIRTUAL_ENV_PATH = ../../project-virtual-env


receuil:
	. $(VIRTUAL_ENV_PATH)/bin/activate; pandoc receuil-de-connaissances.md -o receuil-de-connaissances.pdf
	@echo
	@echo receuil-de-connaissances.pdf généré.
