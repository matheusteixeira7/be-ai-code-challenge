.PHONY: candidate-bundle

candidate-bundle:
	git archive --format=zip --output=candidate-bundle.zip HEAD \
		':(exclude)INTERVIEWER.md' \
		':(exclude)ticket.md' \
		':(exclude).specs' \
		':(exclude)docs' \
		':(exclude).superpowers' \
		':(exclude)Makefile'
