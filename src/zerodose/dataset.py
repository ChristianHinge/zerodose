"""Dataset class for the ZeroDose project."""
import torchio as tio

from zerodose.processing import Pad
from zerodose.processing import ToFloat32


class SubjectDataset(tio.data.SubjectsDataset):
    """Dataset class for the ZeroDose project."""

    def __init__(self, mri_fnames, mask_fnames, out_fnames):
        """Initialize the dataset."""
        transforms = self._get_augmentation_transform_val()
        subjects = [
            self._make_subject_predict(mr_f, ma_f, ou_f)
            for mr_f, ma_f, ou_f in zip(
                mri_fnames, mask_fnames, out_fnames, strict=True
            )
        ]

        super().__init__(subjects, transforms)

    def _make_subject_dict(self, mr_path, mask_path):
        subject_dict = {}
        mri = mr_path
        mask = mask_path

        subject_dict["mr"] = tio.ScalarImage(mri)
        subject_dict["mask"] = tio.LabelMap(mask)

        return subject_dict

    def _make_subject_predict(self, mr_path, mask_path, out_fname):
        subject_dict = self._make_subject_dict(mr_path, mask_path)
        subject_dict["out_fname"] = out_fname

        return tio.Subject(subject_dict)

    def _get_augmentation_transform_val(self):
        return tio.Compose(
            [
                tio.transforms.ZNormalization(include=["mr"], masking_method="mask"),
                Pad(include=["mr", "mask"]),
                ToFloat32(include=["mr"]),
            ]
        )
