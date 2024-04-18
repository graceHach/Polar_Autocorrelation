from sklearn.cluster import KMeans
import polarAC_utils as pAC
import numpy as np
from sklearn import metrics
import matplotlib.pyplot as plt
import matplotlib
from sklearn.metrics import confusion_matrix, ConfusionMatrixDisplay
import stat_utils as SU


# load the dataset
def main():
    ac_dataset = pAC.read_csv("..\data\contrived_noisy\AC_stats.csv")
    #data_cols = ["num_sign_changes","num_1st_deriv_sign_changes","num_2nd_deriv_sign_changes","Abs_AUC","numerical_tangent"]
    #data_cols = ["num_sign_changes", "num_1st_deriv_sign_changes", "num_2nd_deriv_sign_changes"]
    label_col, data_cols = ac_dataset.columns[0], ac_dataset.columns[1:len(ac_dataset.columns)]
    ac_X = np.array(ac_dataset[data_cols])
    ac_Y = np.array(ac_dataset[label_col])
    ac_classifier = KMeans(n_clusters=4, n_init=10)
    ac_classifier.fit(ac_X)
    labels_ac = ac_classifier.labels_
    AC_score = metrics.rand_score(ac_Y, labels_ac)
    shape_dataset = pAC.read_csv("..\\data\\contrived_noisy\\all_shape_descriptors.csv")
    data_cols2 = ['Area', 'Perim.', 'Major','Minor', 'Angl', 'Circ.', 'Median', 'AR', 'Round', 'Soliditye']
    shape_X = np.array(shape_dataset[data_cols2])
    shape_Y = np.array(shape_dataset['Ground truth crypt number '])
    shape_classifier = KMeans(n_clusters=4, n_init='auto')
    ac_classifier.fit(shape_X)
    labels_shape = ac_classifier.labels_
    shape_score = metrics.rand_score(ac_Y, labels_shape)
    #print(AC_score, shape_score)

    # labels don't match. true labels are 2-5, other labels are 0-3
    labels_ac = [x+2 for x in labels_ac]
    labels_shape = [x+2 for x in labels_shape]

    #labels also aren't in the correct permutation
    labels_ac_corrected = SU.transform_labels(ac_Y, labels_ac)
    labels_shape_corrected = SU.transform_labels(ac_Y, labels_shape)

    fig, (ax1, ax2) = plt.subplots(1, 2,layout="constrained", figsize=(10, 6.5))
    #fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(10, 5.75))
    disp1 = ConfusionMatrixDisplay.from_predictions(ac_Y, labels_ac_corrected, normalize='true', ax=ax1, colorbar=False)
    disp2 = ConfusionMatrixDisplay.from_predictions(shape_Y,labels_shape_corrected, normalize='true', ax=ax2, colorbar=False)


    class_names = ['Two', 'Three', 'Four', 'Five']

    fig.suptitle('Feature Number Classification Confusion Matrix' , fontsize=16, y=0.9)

    ax1.set_title('Using statistics from autocorrelation curve', fontsize=12)
    ax1.set_xticks(np.arange(len(class_names)))
    ax1.set_xticklabels(class_names)
    ax1.set_yticks(np.arange(len(class_names)))
    ax1.set_yticklabels(class_names)
    ax1.set_xlabel('Predicted label')
    ax1.set_ylabel('True label')

    # Plot the second matrix
    ax2.set_title('Using shape descriptors', fontsize=12)
    ax2.set_xticks(np.arange(len(class_names)))
    ax2.set_xticklabels(class_names)
    ax2.set_yticks(np.arange(len(class_names)))
    ax2.set_yticklabels(class_names)
    ax2.set_xlabel('Predicted label')
    ax2.set_ylabel('True label')

    cbar = fig.colorbar(matplotlib.cm.ScalarMappable(), ax=[ax1, ax2], shrink=0.6)
    text = fig.text(.17,.07,f"Accuracy: {AC_score*100:.2f}%", fontsize=14, bbox=dict(facecolor='white', edgecolor='black', boxstyle='round,pad=1'))
    text2 = fig.text(.628, .07, f"Accuracy: {shape_score*100:.2f}%", fontsize=14, bbox=dict(facecolor='white', edgecolor='black', boxstyle='round,pad=1'))
    plt.savefig("..\\doc\\fig4.png")
    print("Figure 4 generated.")

if __name__=="__main__":
    main()



