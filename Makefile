.DEFAULT_GOAL := all
.PHONY: package upload clean all

package:
	zip lambda.zip lambda.py

upload:
	aws s3 cp lambda.zip s3://dockerhubtoslacklambda/

clean:
	rm lambda.zip

all: package upload clean
