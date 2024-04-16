from sklearn.cluster import KMeans
import polarAC_utils as pAC
import numpy as np
from sklearn import metrics

# load the dataset
def main():
    ac_dataset = pAC.read_csv("..\data\contrived_noisy\AC_stats.csv")
    data_cols = ["num_sign_changes","num_1st_deriv_sign_changes","num_2nd_deriv_sign_changes","Abs_AUC","numerical_tangent"]
    ac_X = np.array(ac_dataset[data_cols])
    ac_Y = np.array(ac_dataset['Ground_truth_feature_number'])
    ac_classifier = KMeans(n_clusters=4)
    ac_classifier.fit(ac_X)
    labels_ac = ac_classifier.labels_
    AC_score = metrics.rand_score(ac_Y, labels_ac)
    shape_dataset = pAC.read_csv("..\\data\\contrived_noisy\\all_shape_descriptors.csv")
    data_cols2 = ['Area', 'Perim.', 'Major','Minor', 'Angl', 'Circ.', 'Median', 'AR', 'Round', 'Soliditye']
    shape_X = np.array(shape_dataset[data_cols2])
    shape_Y = np.array(shape_dataset['Ground truth crypt number '])
    shape_classifier = KMeans(n_clusters=4)
    ac_classifier.fit(shape_X)
    labels_shape = ac_classifier.labels_
    shape_score = metrics.rand_score(ac_Y, labels_shape)
    print(AC_score, shape_score)

if __name__=="__main__":
    main()



