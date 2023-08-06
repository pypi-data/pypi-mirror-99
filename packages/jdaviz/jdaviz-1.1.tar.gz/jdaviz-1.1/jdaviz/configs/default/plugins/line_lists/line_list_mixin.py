import astropy.units as u

from jdaviz.core.events import AddLineListMessage

__all__ = ['LineListMixin']


class LineListMixin:
    """
    Line list-related methods and properties for use in the configuration
    helper classes.
    """
    def load_line_list(self, line_table, replace=False):
        """
        Convenience function to get to the viewer function. Also
        broadcasts a message so the line list plugin UI can display lines
        loaded via the notebook.
        """

        # If the helper class has a global redshift (as in Specviz), use it
        if not isinstance(line_table, str):
            if hasattr(self, "_redshift") and "redshift" not in line_table.colnames:
                line_table["redshift"] = u.Quantity(self._redshift)

        lt = self.app.get_viewer('spectrum-viewer').load_line_list(line_table,
                                                                   replace=replace,
                                                                   return_table=True)

        # Preset lists were returning None table despite loading correctly
        if lt is None:
            if replace:
                lt = self.spectral_lines.loc["listname", line_table]
            else:
                lt = self.spectral_lines

        add_line_list_message = AddLineListMessage(table=lt, sender=self)
        self.app.hub.broadcast(add_line_list_message)

    def erase_spectral_lines(self, name=None):
        """Convenience function to get to the viewer function"""
        self.app.get_viewer('spectrum-viewer').erase_spectral_lines(name=name)

    def plot_spectral_line(self, line):
        """Convenience function to get to the viewer function"""
        self.app.get_viewer('spectrum-viewer').plot_spectral_line(line)

    def plot_spectral_lines(self):
        """Convenience function to get to the viewer function"""
        self.app.get_viewer('spectrum-viewer').plot_spectral_lines()

    @property
    def spectral_lines(self):
        return self.app.get_viewer('spectrum-viewer').spectral_lines

    @property
    def available_linelists(self):
        return self.app.get_viewer('spectrum-viewer').available_linelists()
