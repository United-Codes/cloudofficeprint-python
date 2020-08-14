<%!
    # Template configuration. Copy over in your template directory
    # (used with `--template-dir`) and adapt as necessary.
    # Note, defaults are loaded from this distribution file, so your
    # config.mako only needs to contain values you want overridden.
    # You can also run pdoc with `--config KEY=VALUE` to override
    # individual values.

    html_lang = 'en'
    show_inherited_members = False
    extract_module_toc_into_sidebar = True
    list_class_variables_in_index = True
    sort_identifiers = True
    show_type_annotations = True

    # Show collapsed source code block next to each item.
    # Disabling this can improve rendering speed of large modules.
    show_source_code = False

    # If set, format links to objects in online source code repository
    # according to this template. Supported keywords for interpolation
    # are: commit, path, start_line, end_line.
    #git_link_template = 'https://github.com/USER/PROJECT/blob/{commit}/{path}#L{start_line}-L{end_line}'
    #git_link_template = 'https://gitlab.com/USER/PROJECT/blob/{commit}/{path}#L{start_line}-L{end_line}'
    #git_link_template = 'https://bitbucket.org/USER/PROJECT/src/{commit}/{path}#lines-{start_line}:{end_line}'
    #git_link_template = 'https://CGIT_HOSTNAME/PROJECT/tree/{path}?id={commit}#n{start-line}'
    git_link_template = None
%>
