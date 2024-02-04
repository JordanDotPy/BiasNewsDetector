#!/bin/bash
docker run -v $(pwd)/data:/code/data -v $(pwd)/doc2vec_testing:/code/doc2vec_testing -it bias_news_detector bash