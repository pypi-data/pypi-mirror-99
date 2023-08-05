import json
import os

import pytest
from click.testing import CliRunner
from demisto_sdk.__main__ import main
from demisto_sdk.commands.common import tools
from demisto_sdk.commands.common.constants import (PACK_METADATA_SUPPORT,
                                                   PACK_METADATA_TAGS,
                                                   PACK_METADATA_USE_CASES,
                                                   PACKS_README_FILE_NAME,
                                                   XSOAR_SUPPORT)
from demisto_sdk.commands.common.errors import Errors
from demisto_sdk.commands.common.hook_validations.base_validator import \
    BaseValidator
from demisto_sdk.commands.common.hook_validations.pack_unique_files import \
    PackUniqueFilesValidator
from demisto_sdk.commands.common.legacy_git_tools import git_path
from git import GitCommandError
from TestSuite.test_tools import ChangeCWD

VALIDATE_CMD = "validate"
PACK_METADATA_PARTNER = {
    "name": "test",
    "description": "test",
    "support": "partner",
    "currentVersion": "1.0.1",
    "author": "bar",
    "categories": [
        "Data Enrichment & Threat Intelligence"
    ],
    "tags": [],
    "useCases": [],
    "keywords": [],
    "price": 2,
    "email": "some@mail.com",
    "url": "https://www.paloaltonetworks.com/cortex"
}


class TestPackUniqueFilesValidator:
    FILES_PATH = os.path.normpath(os.path.join(__file__, f'{git_path()}/demisto_sdk/tests', 'test_files'))
    FAKE_PACK_PATH = os.path.join(FILES_PATH, 'fake_pack')
    FAKE_PATH_NAME = 'fake_pack'
    validator = PackUniqueFilesValidator(FAKE_PATH_NAME)
    validator.pack_path = FAKE_PACK_PATH

    def test_is_error_added_name_only(self):
        self.validator._add_error(('boop', '101'), 'file_name')
        assert f'{self.validator.pack_path}/file_name: [101] - boop\n' in self.validator.get_errors(True)
        assert f'{self.validator.pack_path}/file_name: [101] - boop\n' in self.validator.get_errors()
        self.validator._errors = []

    def test_is_error_added_full_path(self):
        self.validator._add_error(('boop', '101'), f'{self.validator.pack_path}/file/name')
        assert f'{self.validator.pack_path}/file/name: [101] - boop\n' in self.validator.get_errors(True)
        assert f'{self.validator.pack_path}/file/name: [101] - boop\n' in self.validator.get_errors()
        self.validator._errors = []

    def test_is_file_exist(self):
        assert self.validator._is_pack_file_exists(PACKS_README_FILE_NAME)
        assert not self.validator._is_pack_file_exists('boop')
        self.validator._errors = []

    def test_parse_file_into_list(self):
        assert ['boop', 'sade', ''] == self.validator._parse_file_into_list(PACKS_README_FILE_NAME)
        assert not self.validator._parse_file_into_list('boop')
        self.validator._errors = []

    def test_validate_pack_unique_files(self, mocker):
        mocker.patch.object(BaseValidator, 'check_file_flags', return_value='')
        assert not self.validator.are_valid_files(id_set_validations=False)
        fake_validator = PackUniqueFilesValidator('fake')
        assert fake_validator.are_valid_files(id_set_validations=False)

    def test_validate_pack_metadata(self, mocker):
        mocker.patch.object(BaseValidator, 'check_file_flags', return_value='')
        assert not self.validator.are_valid_files(id_set_validations=False)
        fake_validator = PackUniqueFilesValidator('fake')
        assert fake_validator.are_valid_files(id_set_validations=False)

    def test_validate_partner_contribute_pack_metadata_no_mail_and_url(self, mocker, repo):
        """
        Given
        - Partner contributed pack without email and url.

        When
        - Running validate on it.

        Then
        - Ensure validate found errors.
        """
        pack_metadata_no_email_and_url = PACK_METADATA_PARTNER.copy()
        pack_metadata_no_email_and_url['email'] = ''
        pack_metadata_no_email_and_url['url'] = ''
        mocker.patch.object(tools, 'is_external_repository', return_value=True)
        mocker.patch.object(PackUniqueFilesValidator, '_is_pack_file_exists', return_value=True)
        mocker.patch.object(PackUniqueFilesValidator, 'get_master_private_repo_meta_file', return_value=None)
        mocker.patch.object(PackUniqueFilesValidator, '_read_file_content',
                            return_value=json.dumps(pack_metadata_no_email_and_url))
        mocker.patch.object(BaseValidator, 'check_file_flags', return_value=None)
        pack = repo.create_pack('PackName')
        pack.pack_metadata.write_json(pack_metadata_no_email_and_url)
        with ChangeCWD(repo.path):
            runner = CliRunner(mix_stderr=False)
            result = runner.invoke(main, [VALIDATE_CMD, '-i', pack.path], catch_exceptions=False)
        assert 'Contributed packs must include email or url' in result.stdout

    def test_validate_partner_contribute_pack_metadata_price_change(self, mocker, repo):
        """
        Given
        - Partner contributed pack where price has changed.

        When
        - Running validate on it.

        Then
        - Ensure validate found errors.
        """
        pack_metadata_price_changed = PACK_METADATA_PARTNER.copy()
        pack_metadata_price_changed['price'] = 3
        mocker.patch.object(tools, 'is_external_repository', return_value=True)
        mocker.patch.object(PackUniqueFilesValidator, '_is_pack_file_exists', return_value=True)
        mocker.patch.object(PackUniqueFilesValidator, 'get_master_private_repo_meta_file',
                            return_value=PACK_METADATA_PARTNER)
        mocker.patch.object(PackUniqueFilesValidator, '_read_file_content',
                            return_value=json.dumps(pack_metadata_price_changed))
        mocker.patch.object(BaseValidator, 'check_file_flags', return_value=None)
        pack = repo.create_pack('PackName')
        pack.pack_metadata.write_json(pack_metadata_price_changed)
        with ChangeCWD(repo.path):
            runner = CliRunner(mix_stderr=False)
            result = runner.invoke(main, [VALIDATE_CMD, '-i', pack.path], catch_exceptions=False)
        assert 'The pack price was changed from 2 to 3 - revert the change' in result.stdout

    def test_check_timestamp_format(self):
        """
        Given
        - timestamps in various formats.

        When
        - Running check_timestamp_format on them.

        Then
        - Ensure True for iso format and False for any other format.
        """
        fake_validator = PackUniqueFilesValidator('fake')
        good_format_timestamp = '2020-04-14T00:00:00Z'
        missing_z = '2020-04-14T00:00:00'
        missing_t = '2020-04-14 00:00:00Z'
        only_date = '2020-04-14'
        with_hyphen = '2020-04-14T00-00-00Z'
        assert fake_validator.check_timestamp_format(good_format_timestamp)
        assert not fake_validator.check_timestamp_format(missing_t)
        assert not fake_validator.check_timestamp_format(missing_z)
        assert not fake_validator.check_timestamp_format(only_date)
        assert not fake_validator.check_timestamp_format(with_hyphen)

    def test_validate_pack_dependencies_invalid_id_set(self, mocker, repo):
        """
        Given
        - An invalid id set error being raised

        When
        - Running validate_pack_dependencies.

        Then
        - Ensure that the validation fails and that the invalid id set error is printed.
        """

        def error_raising_function(argument):
            raise ValueError("Couldn't find any items for pack 'PackID'. make sure your spelling is correct.")

        mocker.patch.object(tools, 'get_remote_file', side_effect=error_raising_function)
        assert not self.validator.validate_pack_dependencies()
        assert Errors.invalid_id_set()[0] in self.validator.get_errors()

    def test_validate_pack_dependencies_skip_id_set_creation(self, capsys):
        """
        Given
        -  skip_id_set_creation flag set to true.
        -  No id_set file exists

        When
        - Running validate_pack_dependencies.

        Then
        - Ensure that the validation passes and that the skipping message is printed.
        """
        self.validator.skip_id_set_creation = True
        res = self.validator.validate_pack_dependencies()
        self.validator.skip_id_set_creation = False  # reverting to default for next tests
        assert res
        assert "No first level dependencies found" in capsys.readouterr().out

    @pytest.mark.parametrize('usecases, is_valid', [
        ([], True),
        (['Phishing', 'Malware'], True),
        (['NonApprovedUsecase', 'Case Management'], False)
    ])
    def test_is_approved_usecases(self, repo, usecases, is_valid):
        """
        Given:
            - Case A: Pack without usecases
            - Case B: Pack with approved usecases (Phishing and Malware)
            - Case C: Pack with non-approved usecase (NonApprovedUsecase) and approved usecase (Case Management)

        When:
            - Validating approved usecases

        Then:
            - Case A: Ensure validation passes as there are no usecases to verify
            - Case B: Ensure validation passes as both usecases are approved
            - Case C: Ensure validation fails as it contains a non-approved usecase (NonApprovedUsecase)
                      Verify expected error is printed
        """
        pack_name = 'PackName'
        pack = repo.create_pack(pack_name)
        pack.pack_metadata.write_json({
            PACK_METADATA_USE_CASES: usecases,
            PACK_METADATA_SUPPORT: XSOAR_SUPPORT,
            PACK_METADATA_TAGS: []
        })
        self.validator.pack_path = pack.path
        assert self.validator._is_approved_usecases() == is_valid
        if not is_valid:
            assert 'The pack metadata contains non approved usecases: NonApprovedUsecase' in self.validator.get_errors()

    @pytest.mark.parametrize('tags, is_valid', [
        ([], True),
        (['Machine Learning', 'Spam'], True),
        (['NonApprovedTag', 'GDPR'], False)
    ])
    def test_is_approved_tags(self, repo, tags, is_valid):
        """
        Given:
            - Case A: Pack without tags
            - Case B: Pack with approved tags (Machine Learning and Spam)
            - Case C: Pack with non-approved usecase (NonApprovedTag) and approved usecase (GDPR)

        When:
            - Validating approved usecases

        Then:
            - Case A: Ensure validation passes as there are no usecases to verify
            - Case B: Ensure validation passes as both usecases are approved
            - Case C: Ensure validation fails as it contains a non-approved usecase (NonApprovedTag)
                      Verify expected error is printed
        """
        pack_name = 'PackName'
        pack = repo.create_pack(pack_name)
        pack.pack_metadata.write_json({
            PACK_METADATA_USE_CASES: [],
            PACK_METADATA_SUPPORT: XSOAR_SUPPORT,
            PACK_METADATA_TAGS: tags
        })
        self.validator.pack_path = pack.path
        assert self.validator._is_approved_tags() == is_valid
        if not is_valid:
            assert 'The pack metadata contains non approved tags: NonApprovedTag' in self.validator.get_errors()

    @pytest.mark.parametrize('type, is_valid', [
        ('community', True),
        ('partner', True),
        ('xsoar', True),
        ('someName', False),
        ('test', False),
        ('developer', True)
    ])
    def test_is_valid_support_type(self, repo, type, is_valid):
        """
        Given:
            - Pack with support type in the metadata file.

        When:
            - Running _is_valid_support_type.

        Then:
            - Ensure True when the support types are valid, else False with the right error message.
        """
        pack_name = 'PackName'
        pack = repo.create_pack(pack_name)
        pack.pack_metadata.write_json({
            PACK_METADATA_USE_CASES: [],
            PACK_METADATA_SUPPORT: type
        })

        self.validator.pack_path = pack.path
        assert self.validator._is_valid_support_type() == is_valid
        if not is_valid:
            assert 'Support field should be one of the following: xsoar, partner, developer or community.' in \
                   self.validator.get_errors()

    def test_get_master_private_repo_meta_file_running_on_master(self, mocker, repo, capsys):
        """
        Given:
            - A repo which runs on master branch

        When:
            - Running get_master_private_repo_meta_file.

        Then:
            - Ensure result is None and the appropriate skipping message is printed.
        """
        pack_name = 'PackName'
        pack = repo.create_pack(pack_name)
        pack.pack_metadata.write_json(PACK_METADATA_PARTNER)

        class MyRepo:
            active_branch = 'master'

        mocker.patch('demisto_sdk.commands.common.hook_validations.pack_unique_files.Repo', return_value=MyRepo)
        res = self.validator.get_master_private_repo_meta_file(str(pack.pack_metadata.path))
        assert not res
        assert "Running on master branch - skipping price change validation" in capsys.readouterr().out

    def test_get_master_private_repo_meta_file_getting_git_error(self, repo, capsys, mocker):
        """
        Given:
            - A repo which runs on non-master branch.
            - git.show command raises GitCommandError.

        When:
            - Running get_master_private_repo_meta_file.

        Then:
            - Ensure result is None and the appropriate skipping message is printed.
        """
        pack_name = 'PackName'
        pack = repo.create_pack(pack_name)
        pack.pack_metadata.write_json(PACK_METADATA_PARTNER)

        class MyRepo:
            active_branch = 'not-master'

            class gitClass:
                def show(self, var):
                    raise GitCommandError("A", "B")

            git = gitClass()

        mocker.patch('demisto_sdk.commands.common.hook_validations.pack_unique_files.Repo', return_value=MyRepo)
        res = self.validator.get_master_private_repo_meta_file(str(pack.pack_metadata.path))
        assert not res
        assert "Got an error while trying to connect to git" in capsys.readouterr().out

    def test_get_master_private_repo_meta_file_file_not_found(self, mocker, repo, capsys):
        """
        Given:
            - A repo which runs on non-master branch.
            - git.show command returns None.

        When:
            - Running get_master_private_repo_meta_file.

        Then:
            - Ensure result is None and the appropriate skipping message is printed.
        """
        pack_name = 'PackName'
        pack = repo.create_pack(pack_name)
        pack.pack_metadata.write_json(PACK_METADATA_PARTNER)

        class MyRepo:
            active_branch = 'not-master'

            class gitClass:
                def show(self, var):
                    return None

            git = gitClass()

        mocker.patch('demisto_sdk.commands.common.hook_validations.pack_unique_files.Repo', return_value=MyRepo)
        res = self.validator.get_master_private_repo_meta_file(str(pack.pack_metadata.path))
        assert not res
        assert "Unable to find previous pack_metadata.json file - skipping price change validation" in \
               capsys.readouterr().out
