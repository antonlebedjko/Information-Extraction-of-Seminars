ontology_tree = {

    'Science & Enginnering School': {
                'Computer Science': ['software', 'object-oriented', 'architecture', 'design', 'product', 'development', 
                                         'artificial', 'intelligence', 'machine learning', 'ai', 'robotics', 'vision',
                                         'nlp', 'natural language processing', 'ieee', 'navigation', 'robot',
                                         'humanoid', 'autonomous', 'knowledge', 'language', 'decision', 'recognition',
                                         'classification', 'prediction'],


                'Biology': ['bio', 'disease', 'immune', 'immunomodulation', 'biological', 'genome',
                                     'biochemistry', 'molecules', 'medicine', 'clinic', 'cancer', 'health'],
                

                'Chemistry': ['chemistry', 'drugs', 'polymers', 'graft', 'extruders', 'nanotechnology',
                                     'fluids', 'thermodynamic', 'microemulsions', 'flourescence', 'water',
                                     'dissolved'],
                

                'Electronics': ['semiconductor', 'electronic', 'circuit', 'integrated'],
                

                'Physics': ['physics', 'thermodynamics', 'nanotechnology', 'magnetism', 'frequency',
                                     'nuclear'],            
    },
    'Arts School': {
                'Politics': ['politics', 'social', 'public', 'policy', 'issue', 'environment', 'trend',
                                     'economy', 'media', 'global', 'regulations', 'international', 'crisis',
                                     'activist', 'prospects', 'welfare', 'community', 'movement'],

                'Languages': ['language', 'phonology', 'english', 'writing'],

                'Performing Arts': ['music', 'genre', 'ensemble', 'classical', 'theater']
    },
    
    'Business School': {
                    'Finance' : ['finance', 'stock', 'exchange', 'money', 'investment', 'trader', 'bank', 'trend']
    }
    

}

print(ontology_tree['Arts School']['Languages'])

filtered_word_list = word_list[:] #make a copy of the word_list
for word in word_list: # iterate over word_list
  if word in stopwords.words('english'): 
    filtered_word_list.remove(word) # remove word from filtered_word_list if it is a stopword