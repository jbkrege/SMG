import IPython, numpy as np, matplotlib.pyplot as plt, matplotlib, sklearn, librosa, cmath,math, scipy, time

def sim_matrix(feature_vectors, sample_rate, hop_length, distance_metric = 'cosine', display = False):
    """
        Input:
            feature_vectors - a numpy ndarray MxN, where M is the number of features in each vector and 
            N is the length of the sequence.
            sample_rate - sample rate of the original audio
            hop_length - the length of the hop used in the representation
            distance_metric - which distance metric to use to compute similarity. Defaults to cosine.
            display - whether or not to display the similarity matrix after computing it. Defaults to True.
        Output:
            if display is True, plot the similarity matrix. Along the x and y axis of the similarity matrix, 
            the ticks should be in seconds not in samples. 
            returns sim_matrix - an NxN matrix with the pairwise distance between every feature vector.
    """
    #expects the distance metric to match the metric parameter of pdist
    matrix = scipy.spatial.distance.pdist(np.rot90(feature_vectors, 3), distance_metric)
    

    matrix = scipy.spatial.distance.squareform(matrix)
    
    #find the max of the matrix, as if it were flattened into one long array

    d_max = np.amax(matrix)
    

    similarity_matrix = 1.0 - (matrix / float(d_max))
    
    if display:
                
        skip = feature_vectors.shape[-1] / 10

        plt.xticks(np.arange(0, feature_vectors.shape[-1], skip),
                               ['%.2f' % (i * hop_length / float(sample_rate)) for i in range(feature_vectors.shape[-1])][::skip],
                  rotation='vertical')
        plt.yticks(np.arange(0, feature_vectors.shape[-1], skip),
                               ['%.2f' % (i * hop_length / float(sample_rate)) for i in range(feature_vectors.shape[-1])][::skip])
        
        
        plt.xlabel('Time (s)')
        plt.ylabel('Time (s)')
        plt.title('Similarity matrix')
       
        plt.imshow(similarity_matrix)
       
        
        

    
    
    return similarity_matrix


def cross_sim_matrix(feature_vectors_a, feature_vectors_b, sample_rate, hop_length, distance_metric = 'cosine', display = False):
    """
        Input:
            feature_vectors_a - a numpy ndarray MxN, where M is the number of features in each vector and 
            N is the length of the sequence. Corresponds to the reference song.
            feature_vectors_b - a numpy ndarray MxN, where M is the number of features in each vector and 
            N is the length of the sequence. Corresponds to the cover song.
            sample_rate - sample rate of the original audio
            hop_length - how many samples are in each frame
            distance_metric - which distance metric to use to compute similarity. Defaults to cosine.
            display - whether or not to display the similarity matrix after computing it. Defaults to True.
        Output:
            if display is True, plot the similarity matrix. Along the x and y axis of the similarity matrix, 
            the ticks should be in seconds not in samples. 
            returns cross_sim_matrix - an NxN matrix with the pairwise distance between every feature vector.
    """
    
     #expects the distance metric to match the metric parameter of pdist
    
    matrix = scipy.spatial.distance.cdist(np.rot90(feature_vectors_a, 3), np.rot90(feature_vectors_b, 3),  distance_metric)
    #matrix = scipy.spatial.distance.squareform(matrix)
    
    
    #find the max of the matrix, as if it were flattened into one long array
    d_max = np.amax(matrix)
    
    similarity_matrix = 1.0 - (matrix / float(d_max))
    
    
    if display:
        #do plot stuff
        
        plt.imshow(similarity_matrix)
        skip = feature_vectors_a.shape[-1] / 10
        plt.xticks(np.arange(0, feature_vectors_a.shape[-1], skip),
                               ['%.2f' % (i * hop_length / float(sample_rate)) for i in range(feature_vectors_a.shape[-1])][::skip],
                  rotation='vertical')
        skip = feature_vectors_b.shape[-1] / 10
        plt.yticks(np.arange(0, feature_vectors_b.shape[-1], skip),
                               ['%.2f' % (i * hop_length / float(sample_rate)) for i in range(feature_vectors_b.shape[-1])][::skip])
        plt.xlabel('Time (s)')
        plt.ylabel('Time (s)')
        plt.title('Similarity matrix')

    
    return similarity_matrix
