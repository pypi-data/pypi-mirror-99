import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="neurohive-devops-tools",
    version="0.0.63",
    author="Dmitriy Shelestovskiy",
    author_email="one@sonhador.ru",
    description="Neurohive devops tools",
    long_description=long_description,
    long_description_content_type="text/markdown",
    # url="https://github.com/pypa/sampleproject",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3"
    ],
    python_requires='>=3.6',
    entry_points={
        'console_scripts': [
            'bb-trigger=neurohive.integration.bitbucket:main',
            'bb-check-prs-branch=neurohive.integration.bitbucket:check_branch',
            'bb-create-pr=neurohive.cli:bb_create_pr',
            'bb-create-and-merge-pr=neurohive.cli:bb_create_and_merge_pr',
            'jira-add-comment=neurohive.integration.jirawrap:main',
            'uc-run-build=neurohive.integration.unitycloud:run_build',
            'uc-clone-build-from-branch=neurohive.cli:create_and_build_from_prs',
            "ac-cleanup-builds=neurohive.cli:cleanup_old_appcenter_build",
            "ac-get-dl-link=neurohive.cli:get_ac_dl_link",
            "deploy-ecs-task=neurohive.cli:deploy_ecs_task",
            "compose-to-vars=neurohive.cli:prepare_compose_vars",
            "prepare-ustate-values=neurohive.cli:prepare_ustate_kube_values",
            "update-unity-ios-creds=neurohive.cli:update_unity_creds",
            "show-changelog=neurohive.cli:get_git_changelog",
            "bb-check-branch-exists=neurohive.cli:bb_is_branch_exists",
            "bb-create-branch=neurohive.cli:bb_create_branch",
            "slugify=neurohive.cli:slugify_cmd"
        ]
    },
    install_requires=[
        "requests==2.23.0",
        "urllib3==1.25.10",
        "jira==2.0.0",
        "boto3==1.13.1",
        "PyYAML==5.3.1",
        "kubernetes==11.0.0",
        "tenacity==6.2.0",
        "pyOpenSSL==19.1.0",
        "asana==0.10.2"
    ]
)
