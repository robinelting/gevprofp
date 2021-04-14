def script_aligner(tagged_sentences, subs_text, subs_time):
    """aligns subtitles, timestamps and script into a cohesive dictionary
    :param tagged_sentences: list of tagged script sentences
    :param subs_text: preprocessed subtitles
    :param subs_time: preprocessed timestamps
    """
    sub_total = 0
    sub_total_correct = 0
    for sub_text, time in zip(subs_text, subs_time):
        sub_set = set(re.split(r'\s+', sub_text))
        resemblance_high = 0
        best_resemblance = ''
        for script in tagged_sentences:
            if script[0] == 'D':
                script[1] = script[1].lower()
                script_set = set(re.split(r'\s+', script[1]))
                resemblance = sub_set.intersection(script_set)
                resemblance_correct = len(resemblance) / len(sub_set)
                if resemblance_correct > 0.6:
                    if resemblance_correct > resemblance_high:
                        resemblance_high = resemblance_correct
                        best_resemblance = resemblance
                        best_resemblance_index = tagged_sentences.index(script)
                        tagged_sentences[best_resemblance_index].append(
                            sub_text)
                        tagged_sentences[best_resemblance_index].append(time)

        sub_total += len(sub_set)
        sub_total_correct += len(best_resemblance)
    print("Total amount of words in subtitles: {}\n"
          "Total amount of words that match between script and subtitles: {}\n"
          "Percentage of matches between script and subtitles: {}%\n"
          .format(sub_total, sub_total_correct, sub_total_correct /
                  sub_total*100))

    for item in tagged_sentences:
        if len(item) > 4:
            del item[4:]

    return tagged_sentences