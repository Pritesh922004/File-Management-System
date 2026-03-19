import streamlit as st

from File_Managment import (
    append_file_content,
    create_file,
    create_folder,
    display_path,
    get_dashboard_stats,
    list_files,
    list_folders,
    read_file_content,
    remove_file,
    remove_folder,
    rename_file,
    rename_folder,
    BASE_PATH,
    write_file_content,
)


st.set_page_config(page_title='Modern File Manager', page_icon='🗂️', layout='wide')

st.markdown(
    """
    <style>
    .stApp {background: linear-gradient(135deg, #f8fafc 0%, #eef2ff 100%);}
    .block-container {padding-top: 1.8rem; padding-bottom: 2rem;}
    .glass {background: rgba(255,255,255,.82); border: 1px solid rgba(124,58,237,.14);
        border-radius: 22px; padding: 1.2rem 1.3rem; box-shadow: 0 18px 40px rgba(15,23,42,.08);}
    .hero-title {font-size: 2rem; font-weight: 800; color: #111827; margin: 0;}
    .hero-text {color: #475467; margin-top: .35rem;}
    </style>
    """,
    unsafe_allow_html=True,
)


def notify(kind: str, message: str) -> None:
    st.session_state['notice'] = (kind, message)


def show_notice() -> None:
    notice = st.session_state.pop('notice', None)
    if notice:
        getattr(st, notice[0])(notice[1])


def options(paths):
    return [display_path(path) for path in paths]


def refresh_after(action, success_message: str):
    try:
        action()
        notify('success', success_message)
    except Exception as err:
        notify('error', str(err))
    st.rerun()


show_notice()
folders = list_folders()
files = list_files()
stats = get_dashboard_stats()
folder_names = options(folders)
file_names = options(files)

with st.sidebar:
    st.title('🗂️ File Manager')
    page = st.radio('Navigation', ['Dashboard', 'Folders', 'Files', 'Editor'])
    st.caption(f'Workspace: `{BASE_PATH}`')
    if st.button('Refresh', use_container_width=True):
        st.rerun()

st.markdown("<div class='glass'><p class='hero-title'>Modern File Manager</p><p class='hero-text'>A clean Streamlit UI to manage folders, files, and content in your project.</p></div>", unsafe_allow_html=True)
col1, col2, col3 = st.columns(3)
col1.metric('Folders', stats['folders'])
col2.metric('Files', stats['files'])
col3.metric('Project', BASE_PATH.name)

if page == 'Dashboard':
    left, right = st.columns(2)
    with left:
        st.subheader('📁 Folders')
        st.write(folder_names[:12] or ['No folders found'])
    with right:
        st.subheader('📄 Files')
        st.write(file_names[:12] or ['No files found'])

elif page == 'Folders':
    tab1, tab2, tab3 = st.tabs(['Create', 'Rename', 'Delete'])
    with tab1:
        with st.form('create_folder'):
            folder_path = st.text_input('Folder path', placeholder='docs/new_folder')
            if st.form_submit_button('Create Folder', use_container_width=True):
                refresh_after(lambda: create_folder(folder_path), f"Folder '{folder_path}' created.")
    with tab2:
        if folder_names:
            with st.form('rename_folder'):
                folder_src = st.selectbox('Folder', folder_names)
                folder_new = st.text_input('New name or path')
                if st.form_submit_button('Rename Folder', use_container_width=True):
                    refresh_after(lambda: rename_folder(folder_src, folder_new), f"Folder renamed to '{folder_new}'.")
        else:
            st.info('No folders available.')
    with tab3:
        if folder_names:
            with st.form('delete_folder'):
                folder_del = st.selectbox('Folder to delete', folder_names)
                confirm = st.checkbox('Confirm permanent delete')
                if st.form_submit_button('Delete Folder', use_container_width=True):
                    if not confirm:
                        st.warning('Please confirm deletion.')
                    else:
                        refresh_after(lambda: remove_folder(folder_del), f"Folder '{folder_del}' deleted.")
        else:
            st.info('No folders available.')

elif page == 'Files':
    tab1, tab2, tab3 = st.tabs(['Create', 'Rename', 'Delete'])
    with tab1:
        with st.form('create_file'):
            file_path = st.text_input('File path', placeholder='notes.txt')
            if st.form_submit_button('Create File', use_container_width=True):
                refresh_after(lambda: create_file(file_path), f"File '{file_path}' created.")
    with tab2:
        if file_names:
            with st.form('rename_file'):
                file_src = st.selectbox('File', file_names)
                file_new = st.text_input('New name or path')
                if st.form_submit_button('Rename File', use_container_width=True):
                    refresh_after(lambda: rename_file(file_src, file_new), f"File renamed to '{file_new}'.")
        else:
            st.info('No files available.')
    with tab3:
        if file_names:
            with st.form('delete_file'):
                file_del = st.selectbox('File to delete', file_names)
                confirm = st.checkbox('Confirm permanent delete')
                if st.form_submit_button('Delete File', use_container_width=True):
                    if not confirm:
                        st.warning('Please confirm deletion.')
                    else:
                        refresh_after(lambda: remove_file(file_del), f"File '{file_del}' deleted.")
        else:
            st.info('No files available.')

else:
    tab1, tab2, tab3 = st.tabs(['Read', 'Write', 'Append'])
    with tab1:
        if file_names:
            selected = st.selectbox('Choose a file', file_names)
            try:
                content = read_file_content(selected)
                st.text_area('Preview', value=content, height=320)
                st.download_button('Download', data=content, file_name=selected.split('/')[-1].split('\\')[-1], use_container_width=True)
            except Exception as err:
                st.error(str(err))
        else:
            st.info('No files available.')
    with tab2:
        with st.form('write_file'):
            write_path = st.text_input('File path to write')
            write_text = st.text_area('Content', height=220)
            if st.form_submit_button('Write File', use_container_width=True):
                refresh_after(lambda: write_file_content(write_path, write_text), f"Content written to '{write_path}'.")
    with tab3:
        if file_names:
            with st.form('append_file'):
                append_path = st.selectbox('File to append', file_names)
                append_text = st.text_area('Text to append', height=180)
                if st.form_submit_button('Append To File', use_container_width=True):
                    refresh_after(lambda: append_file_content(append_path, append_text), f"Content appended to '{append_path}'.")
        else:
            st.info('No files available.')