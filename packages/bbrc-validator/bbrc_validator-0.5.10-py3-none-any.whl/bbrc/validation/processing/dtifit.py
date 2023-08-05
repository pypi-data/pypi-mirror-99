from ..test import ExperimentTest, Results


class HasCorrectNumberOfItems(ExperimentTest):
    """Passes if a TOPUP_DTIFIT resource is found and such resource contains the
    correct number of items (i.e. 41)."""

    passing = 'BBRCDEV_E02823',
    failing = 'BBRCDEV_E02824',
    CORRECT_NUMBER = 41

    def run(self, experiment_id):
        resource_name = 'TOPUP_DTIFIT'
        data = []

        e = self.xnat_instance.select.experiment(experiment_id)
        files = list(e.resource(resource_name).files())

        res = len(files) == self.CORRECT_NUMBER

        if not res:
            data.append('{} has {} items (different from {})'
                        .format(experiment_id, len(files), self.CORRECT_NUMBER))

        return Results(res, data)


class HasCorrectItems(ExperimentTest):
    """Passes if a TOPUP_DTIFIT resource is found and such resource contains
    the expected items according to the pipeline
    [specifications](https://gitlab.com/bbrc/xnat/xnat-pipelines/-/tree/master/dtifit#outputs)."""

    passing = 'BBRCDEV_E02823',
    failing = 'BBRCDEV_E02824',

    def run(self, experiment_id):
        resource_name = 'TOPUP_DTIFIT'
        expected_items = ['acqparams.txt',
                          'AP_b0.nii.gz',
                          'AP_PA_b0.nii.gz',
                          '*_dn.nii.gz',
                          '*_dn_ec.eddy_command_txt',
                          '*_dn_ec.eddy_movement_rms',
                          '*_dn_ec.eddy_outlier_map',
                          '*_dn_ec.eddy_outlier_n_sqr_stdev_map',
                          '*_dn_ec.eddy_outlier_n_stdev_map',
                          '*_dn_ec.eddy_outlier_report',
                          '*_dn_ec.eddy_parameters',
                          '*_dn_ec.eddy_post_eddy_shell_alignment_parameters',
                          '*_dn_ec.eddy_post_eddy_shell_PE_translation_parameters',
                          '*_dn_ec.eddy_restricted_movement_rms',
                          '*_dn_ec.eddy_rotated_bvecs',
                          '*_dn_ec.eddy_values_of_all_input_parameters',
                          '*_dn_ec_fit_FA.nii.gz',
                          '*_dn_ec_fit_L1.nii.gz',
                          '*_dn_ec_fit_L2.nii.gz',
                          '*_dn_ec_fit_L3.nii.gz',
                          '*_dn_ec_fit_MD.nii.gz',
                          '*_dn_ec_fit_MO.nii.gz',
                          '*_dn_ec_fit_RD.nii.gz',
                          '*_dn_ec_fit_S0.nii.gz',
                          '*_dn_ec_fit_V1.nii.gz',
                          '*_dn_ec_fit_V2.nii.gz',
                          '*_dn_ec_fit_V3.nii.gz',
                          '*_dn_ec.nii.gz',
                          'index.txt',
                          'PA_b0_0.nii.gz',
                          'PA_b0_1.nii.gz',
                          'topup_fieldcoef.nii.gz',
                          'topup.log',
                          'topup_movpar.txt',
                          'unwarped_b0_bet_mask.nii.gz',
                          'unwarped_b0_bet.nii.gz',
                          'unwarped_b0.nii.gz']

        e = self.xnat_instance.select.experiment(experiment_id)
        res = e.resource(resource_name)

        missing = []
        for item in expected_items:
            files = res.files(item).get()
            if not files:
                missing.append(item)

        if missing:
            return Results(False, data=missing)

        return Results(True, data=[])

    def report(self):
        report = []
        if not self.results.has_passed:
            report.append('Missing items: {}.'
                          .format(self.results.data).replace('\'', '`'))
        return report


class HasCorrectANTsVersion(ExperimentTest):
    """This test checks the version of ANTs used. Passes if TOPUP_DTIFIT outputs
    were created using the expected version (`2.3.1.0.post149-gd15f7`)."""

    passing = 'BBRCDEV_E02820',
    failing = 'BBRCDEV_E00272',

    def run(self, experiment_id):
        resource_name = 'TOPUP_DTIFIT'
        expected_version = 'ANTs Version: 2.3.1.0.post149-gd15f7'

        e = self.xnat_instance.select.experiment(experiment_id)
        log_file = e.resource(resource_name).file('LOGS/{}.log'.format(e.label()))

        if not log_file.exists():
            return Results(False, data=['{} log file not found.'.format(resource_name)])

        log_data = self.xnat_instance.get(log_file.attributes()['URI']).text
        ants_version = [line for line in log_data.splitlines()
                        if line.startswith('ANTs Version')][0]

        if not ants_version or not ants_version.startswith(expected_version):
            return Results(False, data=[ants_version])

        return Results(True, data=[])


class HasCorrectFSLVersion(ExperimentTest):
    """This test checks the version of FSL used. Passes if TOPUP_DTIFIT outputs
    were created using the expected version (`6.0.4:ddd0a010`)."""

    passing = 'BBRCDEV_E02823',
    failing = 'BBRCDEV_E02824',

    def run(self, experiment_id):
        resource_name = 'TOPUP_DTIFIT'
        expected_version = 'FSL Version: 6.0.4:ddd0a010'

        e = self.xnat_instance.select.experiment(experiment_id)
        log_file = e.resource(resource_name).file('LOGS/{}.log'.format(e.label()))

        if not log_file.exists():
            return Results(False, data=['{} log file not found.'.format(resource_name)])

        log_data = self.xnat_instance.get(log_file.attributes()['URI']).text
        fsl_version = [line for line in log_data.splitlines()
                       if line.startswith('FSL Version')][0]

        if not fsl_version or not fsl_version.startswith(expected_version):
            return Results(False, data=[fsl_version])

        return Results(True, data=[])


class DTIFITSnapshotFA(ExperimentTest):
    """This test creates a snapshot of the Fractional Anisotropy (FA) map
    generated by TOPUP_DTIFIT. Passes if the snapshot is created successfully.
    Fails otherwise. Does not tell anything on the segmentation quality."""

    passing = 'BBRCDEV_E02820',
    failing = 'BBRCDEV_E00272',

    def run(self, experiment_id):
        import os
        import tempfile

        resource_name = 'TOPUP_DTIFIT'

        e = self.xnat_instance.select.experiment(experiment_id)
        r = e.resource(resource_name)
        if not r.exists():
            return Results(False, data=['{} resource not found'.format(resource_name)])

        fa_map = list(r.files('*FA.nii.gz'))[0]
        if not fa_map.exists():
            return Results(False, data=['FA map not found.'])

        fd, fa_fp = tempfile.mkstemp(suffix='.nii.gz')
        os.close(fd)
        fa_map.get(dest=fa_fp)

        from nilearn import plotting
        paths = []
        for each in 'xyz':
            fd, path = tempfile.mkstemp(suffix='.jpg')
            os.close(fd)
            paths.append(path)
            im = plotting.plot_stat_map(fa_fp,
                                        draw_cross=False,
                                        black_bg=True,
                                        bg_img=None,
                                        display_mode=each,
                                        cut_coords=10)
            im.savefig(path)

        return Results(True, data=paths)

    def report(self):
        report = []
        if self.results.has_passed:
            for path in self.results.data:
                report.append('![snapshot]({})'.format(path))
        else:
            report = self.results.data

        return report


class DTIFITSnapshotRGB(ExperimentTest):
    """This test creates an RGB snapshot of the principal eigenvector (V1) map
    generated by TOPUP_DTIFIT. Passes if the snapshot is created successfully.
    Fails otherwise. Does not tell anything on the segmentation quality."""

    passing = 'BBRCDEV_E02820',
    failing = 'BBRCDEV_E00272',

    def run(self, experiment_id):
        import os
        import tempfile

        resource_name = 'TOPUP_DTIFIT'

        e = self.xnat_instance.select.experiment(experiment_id)
        r = e.resource(resource_name)
        if not r.exists():
            return Results(False, data=['{} resource not found'.format(resource_name)])

        v1_map = list(r.files('*V1.nii.gz'))[0]
        if not v1_map.exists():
            return Results(False, data=['V1 map not found.'])

        fd, v1_fp = tempfile.mkstemp(suffix='.nii.gz')
        os.close(fd)
        v1_map.get(dest=v1_fp)

        import nibabel as nib
        import numpy as np
        from matplotlib import pyplot as plt
        data = nib.load(v1_fp).dataobj
        plt.rcParams['figure.facecolor'] = 'black'

        paths = []
        fd, path = tempfile.mkstemp(suffix='.jpg')
        os.close(fd)
        paths.append(path)

        fig = plt.figure(dpi=300)
        slices = range(10, data.shape[2] - 10, int(data.shape[2] / 12.0))
        border_w = 25
        border_h = 5
        for i, slice_index in enumerate(slices):
            fig.add_subplot(1, len(slices), i + 1)
            test = np.flip(np.swapaxes(np.abs(data[:, :, slice_index, :]), 0, 1), 0)
            w, h, _ = test.shape
            plt.imshow(test[border_h:h - border_h, border_w: w - border_w, :],
                       interpolation='none')
            plt.axis('off')

        fig.savefig(path,
                    facecolor=fig.get_facecolor(),
                    bbox_inches='tight',
                    transparent=True,
                    pad_inches=0)

        fd, path = tempfile.mkstemp(suffix='.jpg')
        os.close(fd)
        paths.append(path)

        fig = plt.figure(dpi=300)
        slices = range(10, data.shape[1] - 10, int(data.shape[1] / 12.0))
        border_w = 25
        border_h = 0
        for i, slice_index in enumerate(slices):
            fig.add_subplot(1, len(slices), i + 1)
            test = np.flip(np.swapaxes(np.abs(data[:, slice_index, :, :]), 0, 1), 0)
            h, w, _ = test.shape
            plt.imshow(test[border_h:h - border_h, border_w: w - border_w, :],
                       interpolation='none')  # black_bg=True)
            plt.axis('off')

        fig.savefig(path,
                    facecolor=fig.get_facecolor(),
                    bbox_inches='tight',
                    transparent=True,
                    pad_inches=0)

        return Results(True, data=paths)

    def report(self):
        report = []
        if self.results.has_passed:
            for path in self.results.data:
                report.append('![snapshot]({})'.format(path))
        else:
            report = self.results.data

        return report


class DTIFITSnapshotTOPUP(ExperimentTest):
    """This test creates an snapshot of the distortion correction by TOPUP. The
    `TOPUP`-corrected version of the image (red colormap) is overlaid with the
    original image (green colormap). Passes if the snapshot is created successfully.
    Fails otherwise. Does not tell anything on the segmentation quality."""

    passing = 'BBRCDEV_E02823',
    failing = 'BBRCDEV_E02824',

    def run(self, experiment_id):
        import os
        import tempfile

        if os.getenv('SKIP_SNAPSHOTS_TESTS') == 'True':
            return Results(experiment_id == self.passing[0],
                           data=['Skipping it. (SKIP_SNAPSHOTS_TESTS)'])

        resource_name = 'TOPUP_DTIFIT'

        e = self.xnat_instance.select.experiment(experiment_id)
        r = e.resource(resource_name)
        if not r.exists():
            return Results(False, data=['{} resource not found'.format(resource_name)])

        fpaths = []
        for fname in ['PA_b0_0.nii.gz', 'unwarped_b0.nii.gz']:
            f = r.file(fname)
            if not f.exists():
                return Results(False, data=['`{}` file not found'.format(fname)])
            fd, fp = tempfile.mkstemp(suffix='.nii.gz')
            os.close(fd)
            f.get(dest=fp)
            fpaths.append(fp)

        from . import topup_snapshot
        snaps = topup_snapshot(pre_fp=fpaths[0], post_fp=fpaths[1])

        return Results(True, data=snaps)

    def report(self):
        report = []
        if self.results.has_passed:
            for path in self.results.data:
                report.append('![snapshot]({})'.format(path))
        else:
            report = self.results.data

        return report


class HasFewNegativeVoxelsInMD(ExperimentTest):
    """DWI denoising step using a Rician noise model (ANTs) introduces some dark
    areas artifacts in denoised images, mostly around the ventricles walls, which
    may propagate to pipeline resulting maps, presenting an abnormal amount of
    voxels with negative values. This test counts the voxels with negative values
    the Mean Diffusivity (MD) map has. Fails if the number of negative voxels
    found is higher than 500. Passes otherwise."""

    passing = 'BBRCDEV_E02823',
    failing = 'BBRCDEV_E02824',

    def run(self, experiment_id):
        import os
        import tempfile

        resource_name = 'TOPUP_DTIFIT'
        negative_voxels_threshold = 500

        e = self.xnat_instance.select.experiment(experiment_id)
        r = e.resource(resource_name)
        if not r.exists():
            return Results(False, data=['{} resource not found'.format(resource_name)])

        md_map = list(r.files('*_MD.nii.gz'))[0]
        if not md_map.exists():
            return Results(False, data=['MD map not found.'])

        fd, md_fp = tempfile.mkstemp(suffix='.nii.gz')
        os.close(fd)
        md_map.get(dest=md_fp)

        import nibabel as nib
        import numpy as np
        md_img = np.asarray(nib.load(md_fp).dataobj)
        negative_voxels = len(md_img[md_img < 0])

        os.remove(md_fp)

        if negative_voxels > negative_voxels_threshold:
            return Results(False, data=[negative_voxels])

        return Results(True, data=[negative_voxels])

    def report(self):
        report = []
        if not self.results.has_passed:
            report.append('MD map has {} voxels with negative values.'
                          .format(self.results.data[0]))
        return report
