import os
from dataclasses import dataclass
from typing import Callable

import ipyfilechooser
from ipywidgets import HTML, Button, HBox, Layout, Output, VBox
from penelope.corpus import VectorizedCorpus, load_corpus
from penelope.utility import default_data_folder, getLogger, right_chop

from ..utility import shorten_filechooser_label

logger = getLogger('penelope')

# pylint: disable=attribute-defined-outside-init, too-many-instance-attributes


debug_view = Output(layout={'border': '1px solid black'})


@dataclass
class LoadGUI:

    default_corpus_folder: str
    filename_pattern: str
    load_callback: Callable[[str, str], VectorizedCorpus]
    done_callback: Callable[[VectorizedCorpus, str, str], None]

    _corpus_filename: ipyfilechooser.FileChooser = None
    _alert: HTML = HTML('.')
    _load_button = Button(
        description='Load',
        button_style='Success',
        layout=Layout(width='115px', background_color='blue'),
        disabled=True,
    )

    @debug_view.capture(clear_output=True)
    def _load_handler(self, _):
        try:
            if not self.corpus_filename or not os.path.isfile(self.corpus_filename):
                self.warn("👎 Please select a valid corpus file 👎")
                return
            self.warn('Please wait')
            self._load_button.description = "Loading..."
            self._load_button.disabled = True
            folder, filename = os.path.split(self.corpus_filename)
            tag = right_chop(filename, self.filename_pattern[1:])
            corpus = self.load_callback(folder=folder, tag=tag)
            self.done_callback(corpus, corpus_folder=folder, corpus_tag=tag)
        except (ValueError, FileNotFoundError, Exception) as ex:
            logger.error(ex)
            self.warn(f"‼ ‼ {ex} ‼ ‼</b>")
        finally:
            self.warn('✔')
            self._load_button.disabled = False
            self._load_button.description = "Load"

    def file_select_callback(self, _: ipyfilechooser.FileChooser):
        self._load_button.disabled = False
        self.alert('✔')

    def setup(self):
        self._corpus_filename: ipyfilechooser.FileChooser = ipyfilechooser.FileChooser(
            path=self.default_corpus_folder or default_data_folder(),
            filter_pattern=self.filename_pattern,
            title='<b>Corpus file (*vectorizer_data.pickle)</b>',
            show_hidden=False,
            select_default=True,
            use_dir_icons=True,
            show_only_dirs=False,
        )
        shorten_filechooser_label(self._corpus_filename, 50)
        self._load_button.on_click(self._load_handler)
        self._corpus_filename.register_callback(self.file_select_callback)
        return self

    def layout(self):
        return VBox(
            [
                HBox(
                    [
                        VBox([self._corpus_filename]),
                        VBox([self._alert, self._load_button]),
                    ]
                )
                # view,
            ]
        )

    @property
    def corpus_filename(self):
        return self._corpus_filename.selected

    def alert(self, msg: str):
        self._alert.value = msg

    def warn(self, msg: str):
        self.alert(f"<span style='color=red'>{msg}</span>")


def create_load_gui(
    *,
    corpus_folder: str,
    loaded_callback: Callable[[VectorizedCorpus, str, str], None],
):

    filename_pattern = '*_vectorizer_data.pickle'

    # @view.capture(clear_output=True)
    def load_corpus_callback(folder: str, tag: str) -> VectorizedCorpus:

        corpus: VectorizedCorpus = load_corpus(
            folder=folder, tag=tag, n_count=None, n_top=None, axis=None, group_by_year=False
        )

        return corpus

    gui = LoadGUI(
        default_corpus_folder=corpus_folder,
        filename_pattern=filename_pattern,
        load_callback=load_corpus_callback,
        done_callback=loaded_callback,
    ).setup()

    return gui
