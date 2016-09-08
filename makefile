#! SHELL=/bin/sh

supervisorctl = /home/work/supervisor/bin/supervisorctl

erp_restart:
	@for port in {8600..8603}; \
	do\
		${supervisorctl} restart erp:erp-$$port; \
	done

erp_restart1:
	@for port in {8600..8600}; \
	do\
		${supervisorctl} restart erp:erp-$$port; \
	done
