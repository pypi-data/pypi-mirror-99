// Copyright (c) Jupyter Development Team.
// Distributed under the terms of the Modified BSD License.

import {
  ILayoutRestorer,
  JupyterFrontEnd,
  JupyterFrontEndPlugin
} from '@jupyterlab/application';
import { IEditMenu, IMainMenu } from '@jupyterlab/mainmenu';
import {
  ABCWidgetFactory,
  DocumentRegistry,
  IDocumentWidget
} from '@jupyterlab/docregistry';
import { IEditorTracker } from '@jupyterlab/fileeditor';
import { ICommandPalette, WidgetTracker } from '@jupyterlab/apputils';
import { ISearchProviderRegistry } from '@jupyterlab/documentsearch';
import { CommandRegistry } from '@lumino/commands';

import '../style/index.css';
import { SpreadsheetWidget } from './widget';
import { SpreadsheetEditorDocumentWidget } from './documentwidget';
import { SpreadsheetSearchProvider } from './searchprovider';
import { ILauncher } from '@jupyterlab/launcher';
import { spreadsheetIcon } from '@jupyterlab/ui-components';
import { IFileBrowserFactory } from '@jupyterlab/filebrowser';

const paletteCategory = 'Spreadsheet Editor';

const FACTORY = 'Spreadsheet Editor';

/**
 * A widget factory for editors.
 */
export class SpreadsheetEditorFactory extends ABCWidgetFactory<
  IDocumentWidget<SpreadsheetWidget>,
  DocumentRegistry.ICodeModel
> {
  /**
   * Create a new widget given a context.
   */
  protected createNewWidget(
    context: DocumentRegistry.CodeContext
  ): IDocumentWidget<SpreadsheetWidget> {
    const content = new SpreadsheetWidget(context);
    return new SpreadsheetEditorDocumentWidget({ content, context });
  }
}

/**
 * Add File Editor undo and redo widgets to the Edit menu
 */
export function addUndoRedoToEditMenu(
  menu: IMainMenu,
  tracker: WidgetTracker<IDocumentWidget<SpreadsheetWidget>>
) {
  // TODO: why is this going crazy without ts-ignore? help!
  // @ts-ignore
  menu.editMenu.undoers.add({
    tracker,
    undo: widget => {
      widget.content.jexcel.undo();
    },
    redo: widget => {
      widget.content.jexcel.redo();
    }
  } as IEditMenu.IUndoer<IDocumentWidget<SpreadsheetWidget>>);
}

/**
 * Function to create a new untitled text file, given the current working directory.
 */
function createNew(commands: CommandRegistry, cwd: string, ext = 'tsv') {
  return commands
    .execute('docmanager:new-untitled', {
      path: cwd,
      type: 'file',
      ext
    })
    .then(model => {
      return commands.execute('docmanager:open', {
        path: model.path,
        factory: FACTORY
      });
    });
}

/**
 * The command IDs used by the spreadsheet editor plugin.
 */
export namespace CommandIDs {
  export const createNewCSV = 'spreadsheet-editor:create-new-csv-file';

  export const createNewTSV = 'spreadsheet-editor:create-new-tsv-file';
}

/**
 * Add Create New DSV File to the Launcher
 */
export function addCreateNewToLauncher(launcher: ILauncher) {
  launcher.add({
    command: CommandIDs.createNewCSV,
    category: 'Other',
    rank: 3
  });
  launcher.add({
    command: CommandIDs.createNewTSV,
    category: 'Other',
    rank: 3
  });
}

/**
 * Add the New File command
 */
export function addCreateNewCommands(
  commands: CommandRegistry,
  browserFactory: IFileBrowserFactory
) {
  commands.addCommand(CommandIDs.createNewCSV, {
    label: args => (args['isPalette'] ? 'New CSV File' : 'CSV File'),
    caption: 'Create a new CSV file',
    icon: args => (args['isPalette'] ? undefined : spreadsheetIcon),
    execute: args => {
      const cwd = args['cwd'] || browserFactory.defaultBrowser.model.path;
      return createNew(commands, cwd as string, 'csv');
    }
  });
  commands.addCommand(CommandIDs.createNewTSV, {
    label: args => (args['isPalette'] ? 'New TSV File' : 'TSV File'),
    caption: 'Create a new TSV file',
    icon: args => (args['isPalette'] ? undefined : spreadsheetIcon),
    execute: args => {
      const cwd = args['cwd'] || browserFactory.defaultBrowser.model.path;
      return createNew(commands, cwd as string, 'tsv');
    }
  });
}

/**
 * Initialization data for the spreadsheet-editor extension.
 */
const extension: JupyterFrontEndPlugin<void> = {
  id: 'spreadsheet-editor',
  autoStart: true,
  requires: [IEditorTracker, IFileBrowserFactory],
  optional: [
    ICommandPalette,
    ILauncher,
    IMainMenu,
    ILayoutRestorer,
    ISearchProviderRegistry
  ],
  activate: (
    app: JupyterFrontEnd,
    editorTracker: IEditorTracker,
    browserFactory: IFileBrowserFactory,
    palette: ICommandPalette | null,
    launcher: ILauncher | null,
    menu: IMainMenu | null,
    restorer: ILayoutRestorer | null,
    searchregistry: ISearchProviderRegistry | null
  ) => {
    const factory = new SpreadsheetEditorFactory({
      name: FACTORY,
      fileTypes: ['csv', 'tsv', '*'],
      defaultFor: ['csv', 'tsv']
    });

    const tracker = new WidgetTracker<IDocumentWidget<SpreadsheetWidget>>({
      namespace: 'spreadsheet-editor'
    });

    if (restorer) {
      void restorer.restore(tracker, {
        command: 'docmanager:open',
        args: widget => ({ path: widget.context.path, factory: FACTORY }),
        name: widget => widget.context.path
      });
    }

    app.docRegistry.addWidgetFactory(factory);
    const ft = app.docRegistry.getFileType('csv');

    factory.widgetCreated.connect((sender, widget) => {
      // Track the widget.
      void tracker.add(widget);
      // Notify the widget tracker if restore data needs to update.
      widget.context.pathChanged.connect(() => {
        void tracker.save(widget);
      });

      if (ft) {
        widget.title.icon = ft.icon!;
        widget.title.iconClass = ft.iconClass!;
        widget.title.iconLabel = ft.iconLabel!;
      }
    });

    if (searchregistry) {
      searchregistry.register('spreadsheet-editor', SpreadsheetSearchProvider);
    }

    addCreateNewCommands(app.commands, browserFactory);

    if (palette) {
      palette.addItem({
        command: CommandIDs.createNewCSV,
        args: { isPalette: true },
        category: paletteCategory
      });
      palette.addItem({
        command: CommandIDs.createNewTSV,
        args: { isPalette: true },
        category: paletteCategory
      });
    }

    if (launcher) {
      addCreateNewToLauncher(launcher);
    }

    if (menu) {
      addUndoRedoToEditMenu(menu, tracker);
    }
  }
};

export default extension;
