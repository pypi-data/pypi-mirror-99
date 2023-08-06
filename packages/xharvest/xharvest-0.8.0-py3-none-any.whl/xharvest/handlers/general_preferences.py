from xharvest.handlers.base import Handler


class GeneralPreferencesHandler(Handler):

    def bind_data(self):
        self.cbtn_close_to_notification_icon = self.get_widget(
                'cbtn_close_to_notification_icon')
        self.cbtn_close_to_notification_icon.set_active(
                self.preferences.get_minimize_to_tray_icon(),
                )

    def on_spin_timeentriesrefreshinterval_value_changed(self, spin_btn):
        interval = spin_btn.get_value_as_int()
        self.preferences.update_timeentries_refresh_interval(interval)

    def on_close_to_notification(self, cbtn):
        self.preferences.update_minimize_to_tray_icon(cbtn.get_active())
