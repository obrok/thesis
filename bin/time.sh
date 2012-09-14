#!/bin/bash

bin/time_topics data/pap-tagged.txt LdaModel >> results/lda_time_topics
bin/time_topics data/pap-tagged.txt LsiModel >> results/lsi_time_topics
