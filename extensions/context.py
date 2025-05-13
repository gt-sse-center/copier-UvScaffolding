"""Contains the ContextUpdater class."""

import copy
import os
import sys

from pathlib import Path
from typing import Any

from copier_templates_extensions import ContextHook
from dbrownell_Common.Streams.DoneManager import DoneManager
from dbrownell_Common import SubprocessEx


# ----------------------------------------------------------------------
class ContextUpdater(ContextHook):
    """Class that handles the generation of dynamic values that are not stored in the generated _copier conf file."""

    # ----------------------------------------------------------------------
    def __init__(self, *args, **kwargs) -> None:  # noqa: D107
        super().__init__(*args, **kwargs)

        # These values will be populated the first time that `hook` is called.
        self._updated_context: dict[str, Any] | None = None
        self._dest_path: Path | None = None
        self._is_update_invocation: bool | None = None

    # ----------------------------------------------------------------------
    def hook(self, context: dict[str, Any]) -> None:  # noqa: D102
        if self._is_update_invocation is None:
            # This hook is called multiple times. Ensure that all questions have been answered
            # before processing the data.
            if context.get("all_questions_have_been_answered", False) is False:
                return

            # This is the first time that this method is called, update the class variables.
            assert self._updated_context is None, self._updated_context
            assert self._dest_path is None, self._dest_path

            self._updated_context = {}
            self._dest_path = Path(context["_copier_conf"]["dst_path"])
            self._dest_path.mkdir(parents=True, exist_ok=True)

            # During copier's update process, copier will fully generate different template versions
            # in local directories. It will then create a diff between those directories to determine
            # changes that should be applied to the destination directory.
            #
            # The steps that create dynamic data (for example, generating public & private keys) should
            # not be invoked when going through this process, as those changes would result in a diff
            # that would be used to overwrite the existing keys in the destination directory. In
            # other words, a new key pair would be generated every time `copier update` is run. This
            # is not the desired behavior, as the keys should be consistent once created.
            #
            # Detect when we are in the update process and then take care to generate dummy values
            # that will be consistent across invocations, thereby preventing a diff that would
            # overwrite content in the destination directory.
            self._is_update_invocation = context["_folder_name"].startswith("copier.main")

            self._GenerateMinisignKey(context)

        assert self._updated_context is not None
        assert self._dest_path is not None
        assert self._is_update_invocation is not None

        context.update(self._updated_context)

    # ----------------------------------------------------------------------
    # ----------------------------------------------------------------------
    # ----------------------------------------------------------------------
    def _GenerateMinisignKey(self, context: dict[str, Any]) -> None:
        if context.get("sign_artifacts_question", True) is False:
            return

        if self._is_update_invocation or context.get("_sign_artifacts_simulate_keygen", False):
            public_key = "___simulated_minisign_public_key___"
        else:
            assert self._dest_path is not None
            public_key_filename = self._dest_path / "minisign_key.pub"

            with DoneManager.Create(
                sys.stdout,
                "\n\nCreating the Minisign public and private keys...",
                suffix="\n\n\n",
            ) as dm:
                if public_key_filename.is_file():
                    dm.WriteLine("The public key already exists.\n")
                else:
                    command_line = '''uvx --with py-minisign python -c "import minisign; from pathlib import Path; keypair = minisign.KeyPair.generate(); Path('minisign_key.pub').open('wb').write(bytes(keypair.public_key)); Path('minisign_key.pri').open('wb').write(bytes(keypair.secret_key));"'''

                    with dm.YieldStream() as stream:
                        env = copy.deepcopy(os.environ)
                        env.pop("VIRTUAL_ENV", None)

                        dm.result = SubprocessEx.Stream(
                            command_line,
                            stream,
                            cwd=self._dest_path,
                            env=env,
                        )

                        if dm.result != 0:
                            sys.exit(dm.result)

                        dm.WriteLine("The public and private keys have been created.\n")

                assert public_key_filename.is_file(), public_key_filename

            # Read the public key from the file
            key_lines = [
                line.strip()
                for line in public_key_filename.read_text(encoding="utf-8").splitlines()
                if line.strip()
            ]

            assert key_lines
            public_key = key_lines[-1]

        assert self._updated_context is not None
        self._updated_context["sign_artifacts_public_key"] = public_key
