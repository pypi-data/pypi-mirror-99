# pylint: disable=line-too-long
import os
import sys
import re
import shutil
import json
from pathlib import Path
import getpass
import filecmp
import click
import yaml
from yaml.loader import SafeLoader
from colorama import Fore, init, Style, deinit, reinit
from pkg_resources import resource_filename, working_set
from paver.easy import sh
from watchdog.observers.polling import PollingObserver
from watchdog.events import FileSystemEventHandler
from livereload import Server
from petljadoc import themes
from .templateutil import apply_template_dir, default_template_arguments
from .cyr2lat import cyr2latTranslate
from .course import Activity, Lesson, Course, YamlLoger, ExternalLink, ActivityTypeValueError

INDEX_TEMPLATE_HIDDEN = '''
.. toctree:: 
    :hidden:
    :maxdepth: {}

'''
INDEX_TEMPLATE = '''
.. toctree:: 
    :maxdepth: {}

'''
YOUTUBE_TEMPLATE = '''
.. ytpopup:: {}
      :width: 735
      :height: 415
      :align: center
'''
PDF_TEMPLATE = '''
.. raw:: html

  <embed src="{}" width="100%" height="700px" type="application/pdf">
'''
LINK_TEMPLATE = '''
    {}

'''
META_DATA = '''
..
  {}
  {}

'''
INDEX_META_DATA = '''
{}
..  
    {}
    {}
    {}
    {}
    {}
    {}

'''

COLORAMA_INIT = True

TOP_LEVEL = 't'
LESSON_LEVEL = 'l'
ACTIVITY_LEVEL = 'a'

ACTIVITY_TYPES = ['reading', 'video', 'quiz', 'coding-quiz']

# ISO Code : Sphinx language code https://www.sphinx-doc.org/en/master/usage/configuration.html#confval-language
LANGUAGE_META_TAG = {'sr-Cyrl': 'sr_RS', 'sr-Latn': 'sr@latn'}


def check_for_runestone_package():
    #pylint: disable=E1133
    if 'runestone' in {pkg.key for pkg in working_set}:
        print('Please remove the runestone package from your working environment in order to use Petljadoc.')
        exit(-1)


def init_template_arguments(template_dir, defaults, project_type):
    ta = default_template_arguments()
    default_project_name = re.sub(r'\s+', '-', os.path.basename(os.getcwd()))
    ta['project_name'] = _prompt("Project name: (one word, no spaces)",
                                 default=default_project_name, force_default=defaults)
    ta['language'] = _prompt("Project language: (supported languages: en, sr, sr-Cyrl, sr-Latn)",
                             default="en", force_default=defaults)
    ta['language_meta'] =  ta['language']
    if ta['language'] in LANGUAGE_META_TAG:
        ta['language'] = LANGUAGE_META_TAG[ta['language']]
    while ' ' in ta['project_name']:
        ta['project_name'] = click.prompt(
            "Project name: (one word, NO SPACES)")
    ta['project_type'] = project_type
    ta['build_dir'] = "./_build"
    ta['dest'] = "../../static"
    ta['use_services'] = "false"
    ta['author'] = _prompt(
        "Author's name", default=getpass.getuser(), force_default=defaults)
    ta['project_title'] = _prompt("Project title",
                                  default=f"Petlja - {os.path.basename(os.getcwd())}",
                                  force_default=defaults)
    ta['python3'] = "true"
    ta['default_ac_lang'] = _prompt("Default ActiveCode language", default="python",
                                    force_default=defaults)
    ta['basecourse'] = ta['project_name']
    ta['login_req'] = "false"
    ta['master_url'] = "http://127.0.0.1:8000"
    ta['master_app'] = "runestone"
    ta['logging'] = False
    ta['log_level'] = 0
    ta['dburl'] = ""
    ta['enable_chatcodes'] = 'false'
    ta['downloads_enabled'] = 'false'
    ta['templates_path'] = '_templates'
    ta['html_theme_path'] = '_templates/plugin_layouts'
    custom_theme = _prompt("Copy HTML theme into project", type=bool,
                           default=False, force_default=defaults)
    if custom_theme:
        ta['html_theme'] = 'custom_theme'
    else:
        if project_type == 'runestone':
            ta['html_theme'] = 'petljadoc_runestone_theme'
        if project_type == 'course':
            ta['html_theme'] = 'petljadoc_course_theme'
    apply_template_dir(template_dir, '.', ta)
    if custom_theme:
        if project_type == 'runestone':
            theme_path = os.path.join(themes.runestone_theme.get_html_theme_path(),
                                      'runestone_theme')
        else:
            theme_path = os.path.join(themes.runestone_theme.get_html_theme_path(),
                                      'course_theme')
        apply_template_dir(theme_path,
                           os.path.join(ta['html_theme_path'],
                                        ta['html_theme']), {},
                           lambda dir, fname: fname not in ['__init__.py', '__pycache__'])


def _prompt(text, default=None, hide_input=False, confirmation_prompt=False,
            type=None,  # pylint: disable=redefined-builtin
            value_proc=None, prompt_suffix=': ', show_default=True, err=False, show_choices=True,
            force_default=False):
    if default and force_default:
        print(text+prompt_suffix+str(default),
              file=sys.stderr if err else sys.stdout)
        return default
    return click.prompt(text, default=default, hide_input=hide_input,
                        confirmation_prompt=confirmation_prompt, type=type, value_proc=value_proc,
                        prompt_suffix=prompt_suffix, show_default=show_default, err=err,
                        show_choices=show_choices)


@click.group()
def main():
    """
    Petlja's command-line interface for learning content

    For help on specific command, use: petljadoc [COMMAND] --help
    """
    check_for_runestone_package()


@main.command('init-course')
@click.option("--yes", "-y", is_flag=True, help="Answer positive to all confirmation questions.")
@click.option("--defaults", is_flag=True, help="Always select the default answer.")
def init_course(yes, defaults):
    """
    Create a new Course project in your current directory
    """
    template_dir = resource_filename('petljadoc', 'project-templates/course')
    print("This will create a new Runestone project in your current directory.")
    if [f for f in os.listdir() if f[0] != '.']:
        raise click.ClickException("Current directrory in not empty")
    if not yes:
        click.confirm("Do you want to proceed? ", abort=True, default=True)
    init_template_arguments(template_dir, defaults, 'course')


@main.command('init-runestone')
@click.option("--yes", "-y", is_flag=True, help="Answer positive to all confirmation questions.")
@click.option("--defaults", is_flag=True, help="Always select the default answer.")
def init_runestone(yes, defaults):
    """
    Create a new Runestone project in your current directory
    """
    template_dir = resource_filename(
        'petljadoc', 'project-templates/runestone')
    print("This will create a new Runestone project in your current directory.")
    if [f for f in os.listdir() if f[0] != '.']:
        raise click.ClickException("Current directrory in not empty")
    if not yes:
        click.confirm("Do you want to proceed? ", abort=True, default=True)
    init_template_arguments(template_dir, defaults, 'runestone')


def build_or_autobuild(cmd_name, port=None, sphinx_build=False, sphinx_autobuild=False):
    path = project_path()
    if not path:
        raise click.ClickException(
            f"You must be in a Runestone project to execute {cmd_name} command")
    os.chdir(path)
    sys.path.insert(0, str(path))
    from pavement import options as paver_options  # pylint: disable=import-error
    buildPath = Path(paver_options.build.builddir)
    if not buildPath.exists:
        os.makedirs(buildPath)
    args = []
    if sphinx_autobuild:
        args.append(f'--port {port}')
        args.append('--open-browser')
        args.append('--no-initial')
        build_module = "sphinx_autobuild"
    if sphinx_build:
        build_module = "sphinx.cmd.build"
        args.append('-a')
        args.append('-E')
    args.append('-b html')
    args.append(f'-c "{paver_options.build.confdir}"')
    args.append(f'-d "{paver_options.build.builddir}/doctrees"')
    for k, v in paver_options.build.template_args.items():
        args.append(f'-A "{k}={v}"')
    args.append(f'"{paver_options.build.sourcedir}"')
    args.append(f'"{paver_options.build.builddir}"')

    sh(f'"{sys.executable}" -m {build_module} ' + " ".join(args))


@main.command()
@click.option("--port", "-p", default=8000, type=int, help="HTTP port numpber (default 8000)")
def preview(port):
    """
    Build and preview the Runestone project in browser
    """
    p = Path(os.getcwd())
    if p.joinpath('conf-petljadoc.json').exists():
        with open('conf-petljadoc.json') as f:
            data = json.load(f)
            if data["project_type"] == "course":
                prebuild()
                watch_server([os.path.realpath('_sources'),
                              os.path.realpath('_images')])
    build_or_autobuild("preview", port=port, sphinx_build=True)
    build_or_autobuild("preview", port=port, sphinx_autobuild=True)


@main.command()
def publish():
    """
    Build and copy the publish folder (docs)
    """
    build_or_autobuild("publish", sphinx_build=True)
    path = project_path()
    if not path:
        raise click.ClickException(
            "You must be in a Runestone project to execute publish command")
    os.chdir(path)
    sys.path.insert(0, str(path))
    from pavement import options as paver_options  # pylint: disable=import-error
    buildPath = Path(paver_options.build.builddir)
    publishPath = path.joinpath("docs")
    click.echo(f'Publishing to {publishPath}')

    def filter_name(item):
        if item not in {"doctrees", "_sources", ".buildinfo", "search.html",
                        "searchindex.js", "objects.inv", "pavement.py","course-errors.js"}:
            return True

    copy_dir(buildPath, publishPath, filter_name)
    open(publishPath.joinpath(".nojekyll"), "w").close()


@main.command()
def cyr2lat():
    """
    Translate from cyrilic to latin letters. Source folder must end with 'Cyrl'.
    """
    sourcePath = os.getcwd()
    print(sourcePath)
    if sourcePath.endswith('Cyrl'):
        destinationPath = Path(sourcePath.split('Cyrl')[0] + "Lat")
        print(destinationPath)
        cyr2latTranslate(sourcePath, destinationPath)
    else:
        print('Folder name must end with Cyrl')


def build_intermediate(rootPath, first_build=True):
    course, errors = create_course()
    course_errors = handle_errors(errors, first_build)
    if not course_errors:
        template_toc(course)
        if first_build:
            create_or_recreate_dir('_intermediate/')
            create_or_recreate_dir('_build/')
            create_intermediate_folder(course, rootPath, '_intermediate/')
        else:
            create_or_recreate_dir('_tmp/')
            create_intermediate_folder(course, rootPath, '_tmp/')
            smart_reload('_tmp/', '_intermediate/')
            shutil.rmtree('_tmp/')
        course.create_YAML('_build/index.yaml')
    else:
        if first_build:
            exit(-1)


def create_or_recreate_dir(file):
    path = Path(file)
    if path.exists():
        shutil.rmtree(file)
    os.mkdir(file)


def load_data_from_YAML():
    with open('_sources/index.yaml', encoding='utf8') as f:
        try:
            data = yaml.load(f, Loader=SafeLineLoader)
            return {'data': data, 'error': {'status': True, 'atribute': None, 'error': None}}
        except yaml.YAMLError as exc:
            # pylint: disable=E1101
            if hasattr(exc, 'problem_mark'):
                if exc.context:
                    return {'data': None, 'error': {'status': False, 'atribute': None, 'error': ' '.join([str(exc.problem_mark),  str(exc.problem), str(exc.context)])}}
                else:
                    return {'data': None, 'error': {'status': False, 'atribute': None, 'error': ' '.join([str(exc.problem_mark),  str(exc.problem)])}}
            else:
                return {'data': None, 'error': {'status': False, 'atribute': None, 'error': YamlLoger.ERROR_YAML_LOAD}}


def prebuild(first_build=True):
    rootPath = Path(os.getcwd())
    if not rootPath.joinpath('_sources/index.yaml').exists():
        raise click.ClickException(
            "index.yaml is not present in source directory")
    build_intermediate(rootPath, first_build)


def project_path():
    p = Path(os.getcwd())
    while True:
        if p.joinpath('pavement.py').exists() and p.joinpath('conf.py').exists():
            return p
        if p == p.parent:
            return None
        p = p.parent


def create_course():
    global ACTIVITY_TYPES
    error_log = {}
    archived_lessons = []
    active_lessons = []
    external_links = []
    willLearn = []
    requirements = []
    toc = []
    YAML_contet = load_data_from_YAML()
    data, error_log[YamlLoger.YAML_PARSER_ERROR_MSG] = YAML_contet['data'], YAML_contet['error']
    if data:
        try:
            error_log[YamlLoger.ATR_COURSE_ID], courseId = check_component(
                data, TOP_LEVEL, YamlLoger.ATR_COURSE_ID)
            error_log[YamlLoger.ATR_LANG], lang = check_component(
                data, TOP_LEVEL, YamlLoger.ATR_LANG)
            error_log[YamlLoger.ATR_TITLE], title_course = check_component(
                data, TOP_LEVEL, YamlLoger.ATR_TITLE)
            error_log[YamlLoger.ATR_DESC], _ = check_component(
                data, TOP_LEVEL, YamlLoger.ATR_DESC)
            if error_log[YamlLoger.ATR_DESC]['status']:
                desc_line_number = data[YamlLoger.ATR_DESC]['__line__']
                error_log[YamlLoger.ATR_LONG_DESC], longDesc = check_component(
                    data[YamlLoger.ATR_DESC], TOP_LEVEL, YamlLoger.ATR_LONG_DESC, args=[desc_line_number])
                error_log[YamlLoger.ATR_SHORT_DESC], shortDesc = check_component(
                    data[YamlLoger.ATR_DESC], TOP_LEVEL, YamlLoger.ATR_SHORT_DESC, args=[desc_line_number])
                error_log[YamlLoger.ATR_WILL_LEARN], willLearn = check_component(
                    data[YamlLoger.ATR_DESC], TOP_LEVEL, YamlLoger.ATR_WILL_LEARN, args=[desc_line_number])
                error_log[YamlLoger.ATR_REQUIREMENTS], requirements = check_component(
                    data[YamlLoger.ATR_DESC], TOP_LEVEL, YamlLoger.ATR_REQUIREMENTS, args=[desc_line_number])
                error_log[YamlLoger.ATR_TOC], toc = check_component(
                    data[YamlLoger.ATR_DESC], TOP_LEVEL, YamlLoger.ATR_TOC, args=[desc_line_number])
                error_log[YamlLoger.ATR_EXTERNAL_LINK], externalLinks = check_component(
                    data[YamlLoger.ATR_DESC], TOP_LEVEL, YamlLoger.ATR_EXTERNAL_LINK, required=False)

                if externalLinks != '':
                    for i, external_link in enumerate(externalLinks, start=1):
                        order_prefix = str(i)+'_'
                        link_line_number = external_link['__line__']
                        error_log[order_prefix + YamlLoger.ATR_EXTERNAL_LINKS_TEXT], text = check_component(
                            external_link, TOP_LEVEL, YamlLoger.ATR_EXTERNAL_LINKS_TEXT, args=[link_line_number, i])
                        error_log[order_prefix + YamlLoger.ATR_EXTERNAL_LINKS_LINK], link = check_component(
                            external_link, TOP_LEVEL, YamlLoger.ATR_EXTERNAL_LINKS_LINK, args=[link_line_number, i])
                        external_links.append(ExternalLink(text, link))

            error_log[YamlLoger.ATR_LESSONS], _ = check_component(
                data, TOP_LEVEL, YamlLoger.ATR_LESSONS)

            if error_log[YamlLoger.ATR_LESSONS]['status']:
                error_log[YamlLoger.ATR_ARCHIVED_LESSON], archived_lessons_list = check_component(
                    data, TOP_LEVEL, YamlLoger.ATR_ARCHIVED_LESSON, required=False)
                if archived_lessons_list != '':
                    for j, archived_lesson in enumerate(archived_lessons_list, start=1):
                        order_prefix = str(j)+'_'
                        archived_lesson_line = archived_lesson['__line__']
                        error_log[order_prefix+YamlLoger.ATR_ARCHIVED_LESSON_GUID], archived_lesson_guid = check_component(
                            archived_lesson, TOP_LEVEL, YamlLoger.ATR_GUID, args=[archived_lesson_line, j])
                        archived_lessons.append(archived_lesson_guid)

                for i, lesson in enumerate(data['lessons'], start=1):
                    active_activies = []
                    archived_activities = []
                    order_prefix_lesson = str(i)+'_'
                    lesson_line = lesson['__line__']
                    error_log[order_prefix_lesson + YamlLoger.ATR_LESSON_TITLE], title = check_component(
                        lesson, LESSON_LEVEL, YamlLoger.ATR_TITLE, args=[lesson_line, i])
                    error_log[order_prefix_lesson + YamlLoger.ATR_LESSON_FOLDER], folder = check_component(
                        lesson, LESSON_LEVEL, YamlLoger.ATR_FOLDER, args=[lesson_line, i])
                    error_log[order_prefix_lesson + YamlLoger.ATR_LESSON_GUID], guid = check_component(
                        lesson, LESSON_LEVEL, YamlLoger.ATR_LESSON_GUID, args=[lesson_line, i])
                    error_log[order_prefix_lesson + YamlLoger.ATR_LESSON_DESC], description = check_component(
                        lesson, LESSON_LEVEL, YamlLoger.ATR_DESC, required=False)
                    error_log[order_prefix_lesson + YamlLoger.ATR_LESSON_ACTIVITIES], lesson_activities = check_component(
                        lesson, LESSON_LEVEL, YamlLoger.ATR_ACTIVITY, args=[lesson_line, i])
                    error_log[order_prefix_lesson + YamlLoger.ATR_LESSON_ARCHIVED_ACTIVITIES], lesson_archived_activities = check_component(
                        lesson, LESSON_LEVEL, YamlLoger.ATR_ARCHIVED_ACTIVITY, required=False)

                    if lesson_archived_activities != '':
                        for j, archived_activity in enumerate(lesson_archived_activities, start=1):
                            order_prefix_archived_lessons = str(i)+'_'+str(j)+'_'
                            archived_activity_line = archived_activity['__line__']
                            error_log[order_prefix_archived_lessons + YamlLoger.ATR_LESSON_ARCHIVED_ACTIVITIE_GUID], archived_activity_guid = check_component(
                                archived_activity, ACTIVITY_LEVEL, YamlLoger.ATR_GUID, args=[i, j, archived_activity_line])
                            archived_activities.append(archived_activity_guid)

                    if error_log[order_prefix_lesson + YamlLoger.ATR_LESSON_ACTIVITIES]:
                        for j, activity in enumerate(lesson_activities, start=1):
                            order_prefix_activitie = str(i)+'_'+str(j)+'_'
                            activity_line = activity['__line__']
                            try:
                                error_log[order_prefix_activitie +
                                          YamlLoger.ATR_ACTIVITY_TYPE], activity_type = check_component(activity, ACTIVITY_LEVEL, YamlLoger.ATR_ACTIVITY_TYPE, args=[i, j, activity_line])
                                if activity_type not in ACTIVITY_TYPES:
                                    raise ActivityTypeValueError(activity_type)
                                error_log[order_prefix_activitie + YamlLoger.ATR_ACTIVITY_TITLE], activity_title = check_component(
                                    activity, ACTIVITY_LEVEL, YamlLoger.ATR_ACTIVITY_TITLE, args=[i, j, activity_line])
                                error_log[order_prefix_activitie+YamlLoger.ATR_ACTIVITY_GUID], activity_guid = check_component(
                                    activity, ACTIVITY_LEVEL, YamlLoger.ATR_ACTIVITY_GUID, args=[i, j, activity_line])
                                error_log[order_prefix_activitie+YamlLoger.ATR_ACTIVITY_DESC], activity_description = check_component(
                                    activity, ACTIVITY_LEVEL, YamlLoger.ATR_DESC, required=False)
                                if error_log[order_prefix_activitie+YamlLoger.ATR_ACTIVITY_TYPE] and activity_type in ['video']:
                                    error_log[order_prefix_activitie+YamlLoger.ATR_ACTIVITY_SRC], activity_src = check_component(
                                        activity, ACTIVITY_LEVEL, YamlLoger.ATR_URL, args=[i, j, activity_line])
                                elif error_log[order_prefix_activitie+YamlLoger.ATR_ACTIVITY_TYPE] and activity_type in ['reading', 'quiz']:
                                    error_log[order_prefix_activitie+YamlLoger.ATR_ACTIVITY_SRC], activity_src = check_component(
                                        activity, ACTIVITY_LEVEL, YamlLoger.ATR_FILE, args=[i, j, activity_line])
                                elif error_log[order_prefix_activitie+YamlLoger.ATR_ACTIVITY_TYPE] and activity_type in ['coding-quiz']:
                                    error_log[order_prefix_activitie+YamlLoger.ATR_ACTIVITY_SRC], activity_src = check_component(
                                        activity, ACTIVITY_LEVEL, YamlLoger.ATR_ACTIVITY_PROBLEMS, args=[i, j, activity_line])

                            except ActivityTypeValueError as e:
                                error_log[order_prefix_activitie +
                                          YamlLoger.ATR_ACTIVITY_TYPE_VALUE] = {'status': False, 'atribute': None, 'error': YamlLoger.ERROR_MSGS[ACTIVITY_LEVEL][YamlLoger.ATR_ACTIVITY_TYPE_VALUE].format(e.message)}
                                continue

                            else:
                                active_activies.append(Activity(
                                    activity_type, activity_title, activity_src, activity_guid, activity_description))

                    active_lessons.append(
                        Lesson(title, folder, guid, description, archived_activities, active_activies))

            course = Course(courseId, lang, title_course, longDesc, shortDesc, willLearn,
                            requirements, toc, external_links, archived_lessons, active_lessons)

            error_log[YamlLoger.DUPLICATE_GUID] = course.guid_check()
            error_log[YamlLoger.SOURCE_MISSING] = course.source_check()

            return course, error_log

        except TypeError:
            error_log[YamlLoger.YAML_TYPE_ERROR] = {
                'status': False, 'atribute': None, 'error':  YamlLoger.ERROR_MSGS[TOP_LEVEL][YamlLoger.YAML_TYPE_ERROR]}
            return None, error_log
    else:
        return None, error_log


def check_component(dictionary, atr_type, component, required=True, args=None):
    try:
        item = dictionary[component]
    except KeyError:
        if required:
            if args is None:
                args = []
            return {'status': False, 'atribute': None, 'error': YamlLoger.ERROR_MSGS[atr_type][component].format(*args)}, ''
        else:
            return {'status': True, 'atribute': None, 'error': None}, ''
    else:
        return {'status': True, 'atribute': item, 'error': None}, item


def write_to_index(index, course):
    index.write(INDEX_META_DATA.format(rst_title(course.title), course.longDesc.replace('\n', ' '),
                                       course.shortDesc, course.willlearn, course.requirements, course.toc, course.externalLinks))
    index.write(INDEX_TEMPLATE_HIDDEN.format(3))


def handle_errors(errors, first_build):
    error_flag = False
    error_log = []
    for key, value in errors.items():
        if not value['status']:
            error_flag = True
            if key == 'guid_integrity':
                for guid in value['guid_duplicate_list']:
                    error_log.append(
                        YamlLoger.ERROR_MSGS[TOP_LEVEL][YamlLoger.DUPLICATE_GUID].format(guid))
            elif key == 'source_integrity':
                for titile, src in zip(value['missing_activitie_titles'], value['missing_activitie_src']):
                    error_log.append(
                        YamlLoger.ERROR_MSGS[TOP_LEVEL][YamlLoger.SOURCE_MISSING].format(titile, src))
            else:
                error_log.append(value['error'])
    if error_flag:
        error_log = "\n"+"\n".join(error_log)
        print_error(error_log, first_build)
    return error_flag


def print_error(error, first_build):
    global COLORAMA_INIT
    if first_build:
        if COLORAMA_INIT:
            init()
            COLORAMA_INIT = False
        else:
            reinit()
        print(Fore.RED, error)
        print(Style.RESET_ALL)
        deinit()
    else:
        with open("_build/_static/error_log.txt", "w+", encoding="utf-8") as f:
            f.write(error)


def template_toc(course):
    with open('course', mode='w', encoding='utf8') as file:
        file.write(json.dumps(course.to_dict()))


def create_intermediate_folder(course, path, intermediatPath):
    index = open(intermediatPath+'index.rst', mode='w+', encoding='utf-8')
    write_to_index(index, course)
    path = path.joinpath(intermediatPath)
    create_activity_RST(course, index, path, intermediatPath)


def create_activity_RST(course, index, path, intermediatPath):
    for lesson in course.active_lessons:
        copy_dir('_sources/'+lesson.folder, intermediatPath+lesson.folder)
        index.write(' '*4+lesson.title+' <' + lesson.folder + '/index>\n')
        section_index = open(path.joinpath(lesson.folder).joinpath('index.rst'),
                             mode='w+',
                             encoding='utf-8')
        section_index.write(rst_title(lesson.title))
        section_index.write(INDEX_TEMPLATE.format(1))
        for activity in lesson.active_activies:
            if activity.activity_type in ['reading', 'quiz']:
                if activity.get_src_ext() == 'rst':
                    section_index.write(' '*4+activity.src+'\n')
                    with open(intermediatPath+lesson.folder+'/'+activity.src, mode='r+', encoding='utf8') as file:
                        content = file.read()
                        file.seek(0, 0)
                        file.write(META_DATA.format(activity.title,
                                                    activity.activity_type) + content)
                if activity.get_src_ext() == 'pdf':
                    pdf_rst = open(intermediatPath+lesson.folder+'/'+activity.title+'.rst',
                                   mode='w+', encoding='utf-8')
                    pdf_rst.write(rst_title(activity.title))
                    pdf_rst.write(PDF_TEMPLATE.format(
                        '/_static/'+activity.src))
                    section_index.write(' '*4+activity.title+'.rst\n')
            if activity.activity_type == 'video':
                video_rst = open(intermediatPath+lesson.folder+'/'+activity.title+'.rst',
                                 mode='w+', encoding='utf-8')
                video_rst.write(rst_title(activity.title))
                video_rst.write(YOUTUBE_TEMPLATE.format(activity.src))
                section_index.write(' '*4+activity.title+'.rst\n')
            if activity.activity_type == 'coding-quiz':
                coding_quiz_rst = open(intermediatPath+lesson.folder+'/'+activity.title+'.rst',
                                       mode='w+', encoding='utf-8')
                coding_quiz_rst.write(rst_title(activity.title))
                for s in activity.src:
                    coding_quiz_rst.write(LINK_TEMPLATE.format(s))
                section_index.write(' '*4+activity.title+'.rst\n')


def read_course():
    with open('course', mode='r', encoding='utf8') as file:
        course = json.load(file)
        return course


def smart_reload(root_src_dir, root_dst_dir):
    for src_dir, _, files in os.walk(root_dst_dir):
        dst_dir = src_dir.replace(root_dst_dir, root_src_dir, 1)
        for file_ in files:
            src_file = os.path.join(src_dir, file_)
            dst_file = os.path.join(dst_dir, file_)
            if not os.path.exists(dst_file):
                os.remove(src_file)
    for src_dir, _, files in os.walk(root_src_dir):
        dst_dir = src_dir.replace(root_src_dir, root_dst_dir, 1)
        if not os.path.exists(dst_dir):
            os.makedirs(dst_dir)
        for file_ in files:
            src_file = os.path.join(src_dir, file_)
            dst_file = os.path.join(dst_dir, file_)
            if os.path.exists(dst_file):
                if not filecmp.cmp(src_file, dst_file):
                    current_path = Path(os.getcwd())
                    shutil.move(os.path.join(current_path, src_file),
                                os.path.join(current_path, dst_file))
            else:
                shutil.move(src_file, dst_dir)


def copy_dir(src_dir, dest_dir, filter_name=None):
    # print(f"D {src_dir} -> {dest_dir}")
    if not os.path.exists(dest_dir):
        os.makedirs(dest_dir)
    for item in os.listdir(src_dir):
        if filter_name and not filter_name(item):
            continue
        s = os.path.join(src_dir, item)
        if os.path.isdir(s):
            d = os.path.join(dest_dir, item)
            copy_dir(s, d, filter_name)
        else:
            d = os.path.join(dest_dir, item)
            shutil.copyfile(s, d)
            #print(f"C {s} -> {d}")


def rst_title(title):
    title_bar = '='*len(title)+'\n'
    return title_bar + title+'\n' + title_bar


class _WatchdogHandler(FileSystemEventHandler):

    def __init__(self, watcher):
        super(_WatchdogHandler, self).__init__()
        self._watcher = watcher

    def on_any_event(self, event):
        if event.is_directory:
            return
        if event.event_type == 'modified' and event.src_path[-3:] == 'rst':
            try:
                shutil.copyfile(event.src_path, event.src_path.replace(
                    '_sources', '_intermediate'))
            except FileNotFoundError:
                pass
        elif os.path.split(os.path.split(event.src_path)[0])[1] == '_images':
            image_name = os.path.split(event.src_path)[1]
            project_root = Path(os.getcwd())
            build_path_to_image = os.path.join(
                project_root, '_build/_images/' + image_name)
            if event.event_type in ['created', 'modified']:
                if os.path.exists(build_path_to_image):
                    os.remove(build_path_to_image)
                shutil.copy(event.src_path, build_path_to_image)
        else:
            prebuild(False)


class LivereloadWatchdogWatcher(object):
    """
    File system watch dog.
    """

    def __init__(self):
        super(LivereloadWatchdogWatcher, self).__init__()
        self._changed = False

        # Allows the LivereloadWatchdogWatcher
        # instance to set the file which was
        # modified. Used for output purposes only.
        self._action_file = None
        self._observer = PollingObserver()
        self._observer.start()

        # Compatibility with livereload's builtin watcher

        # Accessed by LiveReloadHandler's on_message method to decide if a task
        # has to be added to watch the cwd.
        self._tasks = True

        # Accessed by LiveReloadHandler's watch_task method. When set to a
        # boolean false value, everything is reloaded in the browser ('*').
        self.filepath = None

        # Accessed by Server's serve method to set reload time to 0 in
        # LiveReloadHandler's poll_tasks method.
        self._changes = []
    #pylint: disable=unused-argument

    def watch(self, path, *args, **kwargs):
        event_handler = _WatchdogHandler(self)
        self._observer.schedule(event_handler, path=path, recursive=True)


def watch_server(srcdirList):
    server = Server(
        watcher=LivereloadWatchdogWatcher(),
    )
    for srcdir in srcdirList:
        server.watch(srcdir)


class SafeLineLoader(SafeLoader):
    def construct_mapping(self, node, deep=False):
        mapping = super(SafeLineLoader, self).construct_mapping(
            node, deep=deep)
        mapping['__line__'] = node.start_mark.line + 1
        return mapping
