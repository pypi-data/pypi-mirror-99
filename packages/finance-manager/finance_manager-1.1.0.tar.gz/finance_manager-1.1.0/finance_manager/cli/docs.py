# pylint: disable=no-member
import click
import win32com.client
from finance_manager.database.spec import directorate
from finance_manager.database import DB


@click.command()
@click.argument("template", type=click.Path(exists=True))
@click.argument("folder", type=click.Path(exists=True))
@click.option("--version", "-v", type=str, help="Append a given version identifier.")
@click.option("--disconnect", "-d", is_flag=True, help="Run the Disconnect macro to sever connections.")
@click.pass_obj
def docs(config, template, folder, version, disconnect):
    """
    Generate documentation for each directorate.

    Currently relies on the template having a sheet called 'data_Params', with the columns laid out
    as configured in this source code. Only works on Windows.
    """
    if folder[-1] == '\\':
        folder = folder[:-2]
    with DB(config=config) as db:
        session = db.session()
        directorates = session.query(directorate).filter(
            directorate.director_name.isnot(None)).all()

        # Create an excel app
        xlapp = win32com.client.DispatchEx("Excel.Application")
        xlapp.DisplayAlerts = False
        # Open the workbook in said instance of Excel
        wb = xlapp.workbooks.open(template)
        if disconnect:
            file_password = None
        else:
            file_password = 'pie'
        with click.progressbar(directorates) as bar:
            for d in bar:
                ws = wb.Worksheets("data_Params")
                ws.Range("A2").Value = d.directorate_id
                ws.Range("D2").Value = d.description
                ws.Range("E2").Value = d.director_name
                acad_year = ws.Range("C2").Value
                set_cat_id = ws.Range("B2").Value
                namelist = [d.description, set_cat_id]
                if version is not None:
                    if version[0].lower() == 'v':
                        version = version[1:]
                    version = 'v'+version
                    namelist.append(version)
                filename = folder + '\\' + \
                    ' '.join(namelist) + '.xlsm'
                macro_name = "'" + wb.name + "'!Automation.UpdateRefreshConnections"
                xlapp.Run(macro_name)
                if disconnect:
                    macro_name = "'" + wb.name + "'!Automation.Disconnect"
                    xlapp.Run(macro_name)
                wb.SaveAs(filename, None, file_password)
                if disconnect:
                    # Have to close and reopen as connections severed
                    wb.Close()
                    wb = xlapp.workbooks.open(template)
        xlapp.Quit()
