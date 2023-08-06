from robocorp_ls_core.cache import instance_cache
from robocorp_ls_core.constants import NULL
from robocorp_ls_core.protocols import IMonitor, Sentinel, IConfig, IDocumentSelection
from robocorp_ls_core.robotframework_log import get_logger
from robotframework_ls.impl.robot_workspace import RobotDocument
from typing import Optional, Any, List, Tuple
from robotframework_ls.impl.protocols import (
    IRobotDocument,
    ICompletionContext,
    TokenInfo,
    IRobotWorkspace,
    IKeywordDefinition,
    ILibraryImportNode,
)


log = get_logger(__name__)


class _Memo(object):
    def __init__(self):
        self.clear()

    def clear(self):
        self._followed_imports_variables = {}
        self._followed_imports = {}
        self._completed_libraries = {}

    def follow_import(self, uri: str) -> bool:
        if uri not in self._followed_imports:
            self._followed_imports[uri] = True
            return True

        return False

    def follow_import_variables(self, uri: str) -> bool:
        if uri not in self._followed_imports_variables:
            self._followed_imports_variables[uri] = True
            return True

        return False

    def complete_for_library(self, library_name: str) -> bool:
        if library_name not in self._completed_libraries:
            self._completed_libraries[library_name] = True
            return True

        return False


class BaseContext(object):
    def __init__(self, workspace: IRobotWorkspace, config: IConfig, monitor: IMonitor):
        self._workspace = workspace
        self._config = config
        self._monitor = monitor

    @property
    def monitor(self) -> IMonitor:
        return self._monitor

    @property
    def workspace(self) -> IRobotWorkspace:
        return self._workspace

    @property
    def config(self) -> IConfig:
        return self._config

    def check_cancelled(self) -> None:
        self._monitor.check_cancelled()

    def __typecheckself__(self) -> None:
        from robocorp_ls_core.protocols import check_implements
        from robotframework_ls.impl.protocols import IBaseCompletionContext

        _: IBaseCompletionContext = check_implements(self)


class CompletionContext(object):

    TYPE_TEST_CASE = RobotDocument.TYPE_TEST_CASE
    TYPE_INIT = RobotDocument.TYPE_INIT
    TYPE_RESOURCE = RobotDocument.TYPE_RESOURCE

    def __init__(
        self,
        doc,
        line=Sentinel.SENTINEL,
        col=Sentinel.SENTINEL,
        workspace=None,
        config=None,
        memo=None,
        monitor: IMonitor = NULL,
    ) -> None:
        """
        :param robocorp_ls_core.workspace.Document doc:
        :param int line:
        :param int col:
        :param RobotWorkspace workspace:
        :param robocorp_ls_core.config.Config config:
        :param _Memo memo:
        """

        if col is Sentinel.SENTINEL or line is Sentinel.SENTINEL:
            assert col is Sentinel.SENTINEL, (
                "Either line and col are not set, or both are set. Found: (%s, %s)"
                % (line, col)
            )
            assert line is Sentinel.SENTINEL, (
                "Either line and col are not set, or both are set. Found: (%s, %s)"
                % (line, col)
            )

            # If both are not set, use the doc len as the selection.
            line, col = doc.get_last_line_col()

        memo = _Memo() if memo is None else memo

        sel = doc.selection(line, col)

        self._doc = doc
        self._sel = sel
        self._workspace = workspace
        self._config = config
        self._memo = memo
        self._original_ctx: Optional[CompletionContext] = None
        self._monitor = monitor or NULL

    @property
    def monitor(self) -> IMonitor:
        return self._monitor

    def check_cancelled(self) -> None:
        self._monitor.check_cancelled()

    def create_copy_with_selection(self, line: int, col: int) -> ICompletionContext:
        doc = self._doc
        ctx = CompletionContext(
            doc,
            line=line,
            col=col,
            workspace=self._workspace,
            config=self._config,
            memo=self._memo,
        )
        ctx._original_ctx = self
        return ctx

    def create_copy(self, doc: IRobotDocument) -> ICompletionContext:
        ctx = CompletionContext(
            doc,
            line=0,
            col=0,
            workspace=self._workspace,
            config=self._config,
            memo=self._memo,
        )
        ctx._original_ctx = self
        return ctx

    @property
    def original_doc(self) -> IRobotDocument:
        if self._original_ctx is None:
            return self._doc
        return self._original_ctx.original_doc

    @property
    def original_sel(self) -> IDocumentSelection:
        if self._original_ctx is None:
            return self._sel
        return self._original_ctx.original_sel

    @property
    def doc(self) -> IRobotDocument:
        return self._doc

    @property
    def sel(self) -> IDocumentSelection:
        return self._sel

    @property
    def memo(self) -> Any:
        return self._memo

    @property
    def config(self) -> Optional[IConfig]:
        return self._config

    @property
    def workspace(self) -> IRobotWorkspace:
        return self._workspace

    @instance_cache
    def get_type(self) -> Any:
        return self.doc.get_type()

    @instance_cache
    def get_ast(self) -> Any:
        return self.doc.get_ast()

    @instance_cache
    def get_ast_current_section(self) -> Any:
        """
        :rtype: robot.parsing.model.blocks.Section|NoneType
        """
        from robotframework_ls.impl import ast_utils

        ast = self.get_ast()
        section = ast_utils.find_section(ast, self.sel.line)
        return section

    def get_accepted_section_header_words(self) -> List[str]:
        """
        :rtype: list(str)
        """
        sections = self._get_accepted_sections()
        ret = []
        for section in sections:
            for marker in section.markers:
                ret.append(marker.title())
        ret.sort()
        return ret

    def get_current_section_name(self) -> Optional[str]:
        """
        :rtype: str|NoneType
        """
        section = self.get_ast_current_section()

        section_name = None
        header = getattr(section, "header", None)
        if header is not None:
            try:
                section_name = header.name
            except AttributeError:
                section_name = header.value  # older version of 3.2

        return section_name

    def _get_accepted_sections(self) -> list:
        """
        :rtype: list(robot_constants.Section)
        """
        from robotframework_ls.impl import robot_constants

        t = self.get_type()
        if t == self.TYPE_TEST_CASE:
            return robot_constants.TEST_CASE_FILE_SECTIONS

        elif t == self.TYPE_RESOURCE:
            return robot_constants.RESOURCE_FILE_SECTIONS

        elif t == self.TYPE_INIT:
            return robot_constants.INIT_FILE_SECTIONS

        else:
            log.critical("Unrecognized section: %s", t)
            return robot_constants.TEST_CASE_FILE_SECTIONS

    def get_section(self, section_name) -> Any:
        """
        :rtype: robot_constants.Section
        """
        section_name = section_name.lower()
        accepted_sections = self._get_accepted_sections()

        for section in accepted_sections:
            for marker in section.markers:
                if marker.lower() == section_name:
                    return section
        return None

    @instance_cache
    def get_current_token(self) -> Optional[TokenInfo]:
        from robotframework_ls.impl import ast_utils

        section = self.get_ast_current_section()
        if section is None:
            return None
        return ast_utils.find_token(section, self.sel.line, self.sel.col)

    @instance_cache
    def get_current_variable(self, section=None) -> Optional[TokenInfo]:
        from robotframework_ls.impl import ast_utils

        if section is None:
            section = self.get_ast_current_section()

        if section is None:
            return None
        return ast_utils.find_variable(section, self.sel.line, self.sel.col)

    @instance_cache
    def get_imported_libraries(self) -> Tuple[ILibraryImportNode, ...]:
        from robotframework_ls.impl import ast_utils

        ast = self.get_ast()
        ret = []
        for library_import in ast_utils.iter_library_imports(ast):
            ret.append(library_import.node)
        return tuple(ret)

    @instance_cache
    def get_resource_imports(self):
        from robotframework_ls.impl import ast_utils

        ast = self.get_ast()
        ret = []
        for resource in ast_utils.iter_resource_imports(ast):
            ret.append(resource.node)
        return tuple(ret)

    def token_value_resolving_variables(self, token):
        from robotframework_ls.impl import ast_utils

        if isinstance(token, str):
            token = ast_utils.create_token(token)

        try:
            tokenized_vars = ast_utils.tokenize_variables(token)
        except:
            return token.value  # Unable to tokenize
        parts = []
        for v in tokenized_vars:
            if v.type == v.NAME:
                parts.append(str(v))

            elif v.type == v.VARIABLE:
                # Resolve variable from config
                initial_v = v = str(v)
                if v.startswith("${") and v.endswith("}"):
                    v = v[2:-1]
                    parts.append(self.convert_robot_variable(v, initial_v))
                else:
                    log.info("Cannot resolve variable: %s", v)
                    parts.append(v)  # Leave unresolved.

        joined_parts = "".join(parts)
        return joined_parts

    @instance_cache
    def get_resource_import_as_doc(self, resource_import) -> Optional[IRobotDocument]:
        from robocorp_ls_core import uris
        import os.path
        from robotframework_ls.impl.robot_lsp_constants import OPTION_ROBOT_PYTHONPATH

        ws = self._workspace

        for token in resource_import.tokens:
            if token.type == token.NAME:

                name_with_resolved_vars = self.token_value_resolving_variables(token)

                if not os.path.isabs(name_with_resolved_vars):
                    # It's a relative resource, resolve its location based on the
                    # current file.
                    check_paths = [
                        os.path.join(
                            os.path.dirname(self.doc.path), name_with_resolved_vars
                        )
                    ]
                    config = self.config
                    if config is not None:
                        for additional_pythonpath_entry in config.get_setting(
                            OPTION_ROBOT_PYTHONPATH, list, []
                        ):
                            check_paths.append(
                                os.path.join(
                                    additional_pythonpath_entry, name_with_resolved_vars
                                )
                            )

                else:
                    check_paths = [name_with_resolved_vars]

                for resource_path in check_paths:
                    doc_uri = uris.from_fs_path(resource_path)
                    resource_doc = ws.get_document(doc_uri, accept_from_file=True)
                    if resource_doc is None:
                        continue
                    return resource_doc

                log.info(
                    "Unable to find: %s (checked paths: %s)",
                    name_with_resolved_vars,
                    check_paths,
                )

        return None

    @instance_cache
    def get_resource_imports_as_docs(self) -> Tuple[IRobotDocument, ...]:
        ret: List[IRobotDocument] = []

        # Get keywords from resources
        resource_imports = self.get_resource_imports()
        for resource_import in resource_imports:
            resource_doc = self.get_resource_import_as_doc(resource_import)
            if resource_doc is not None:
                ret.append(resource_doc)

        return tuple(ret)

    def convert_robot_variable(self, var_name, value_if_not_found):
        from robotframework_ls.impl.robot_lsp_constants import OPTION_ROBOT_VARIABLES

        if self.config is None:
            log.info(
                "Config not available while trying to convert variable: %s", var_name
            )
            value = value_if_not_found
        else:
            robot_variables = self.config.get_setting(OPTION_ROBOT_VARIABLES, dict, {})
            value = robot_variables.get(var_name)
            if value is None:
                log.info("Unable to find variable: %s", var_name)
                value = value_if_not_found
        value = str(value)
        return value

    @instance_cache
    def get_current_keyword_definition(self) -> Optional[IKeywordDefinition]:
        """
        Provides the current keyword even if we're in its arguments and not actually
        on the keyword itself.
        """
        from robotframework_ls.impl.find_definition import find_keyword_definition
        from robotframework_ls.impl import ast_utils

        token_info = self.get_current_token()
        if token_info is not None:
            cp: ICompletionContext = self
            while token_info.token.type == token_info.token.EOL:
                sel = cp.sel
                if sel.col > 0:
                    cp = cp.create_copy_with_selection(sel.line, sel.col - 1)
                    token_info = cp.get_current_token()
                else:
                    break

            usage_info = ast_utils.create_keyword_usage_info(
                token_info.stack, token_info.node
            )
            if usage_info is not None:
                token = usage_info.token

                # token line is 1-based and col is 0-based (make both 0-based here).
                line = token.lineno - 1
                col = token.col_offset
                cp = cp.create_copy_with_selection(line, col)
                definitions = find_keyword_definition(
                    cp, TokenInfo(usage_info.stack, usage_info.node, usage_info.token)
                )
                if definitions and len(definitions) >= 1:
                    definition: IKeywordDefinition = next(iter(definitions))
                    return definition
        return None

    def __typecheckself__(self) -> None:
        from robocorp_ls_core.protocols import check_implements

        _: ICompletionContext = check_implements(self)
