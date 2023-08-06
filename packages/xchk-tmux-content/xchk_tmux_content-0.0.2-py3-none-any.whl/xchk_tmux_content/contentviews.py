from xchk_core.contentviews import ContentView
from xchk_core.strats import *

class DoorOutputScrollenCopyModeView(ContentView):
    uid = 'xchk_tmux_content_door_output_scrollen_copy_mode'
    title = 'door output scrollen: copy mode'
    template = 'xchk_tmux_content/door_output_scrollen_copy_mode.html'
    strat = Strategy(refusing_check=TrueCheck(),accepting_check=Negation(TrueCheck()))


class InhoudVanPaneNaarFileSchrijvenView(ContentView):
    uid = 'xchk_tmux_content_inhoud_van_pane_naar_file_schrijven'
    title = 'inhoud van pane naar file schrijven'
    template = 'xchk_tmux_content/inhoud_van_pane_naar_file_schrijven.html'
    strat = Strategy(refusing_check=TrueCheck(),accepting_check=Negation(TrueCheck()))


class PaneOpenenInHuidigeDirectoryView(ContentView):
    uid = 'xchk_tmux_content_pane_openen_in_huidige_directory'
    title = 'pane openen in huidige directory'
    template = 'xchk_tmux_content/pane_openen_in_huidige_directory.html'
    strat = Strategy(refusing_check=TrueCheck(),accepting_check=Negation(TrueCheck()))


class KopierenEnPlakkenView(ContentView):
    uid = 'xchk_tmux_content_kopieren_en_plakken'
    title = 'kopiëren en plakken'
    template = 'xchk_tmux_content/kopieren_en_plakken.html'
    strat = Strategy(refusing_check=TrueCheck(),accepting_check=Negation(TrueCheck()))


class NamedSessionsMakenView(ContentView):
    uid = 'xchk_tmux_content_named_sessions_maken'
    title = '(named) sessions maken'
    template = 'xchk_tmux_content/named_sessions_maken.html'
    strat = Strategy(refusing_check=TrueCheck(),accepting_check=Negation(TrueCheck()))


class PaneTijdelijkMaximaliserenView(ContentView):
    uid = 'xchk_tmux_content_pane_tijdelijk_maximaliseren'
    title = 'pane tijdelijk maximaliseren'
    template = 'xchk_tmux_content/pane_tijdelijk_maximaliseren.html'
    strat = Strategy(refusing_check=TrueCheck(),accepting_check=Negation(TrueCheck()))


class StatusLineItemsView(ContentView):
    uid = 'xchk_tmux_content_status_line_items'
    title = 'status line items'
    template = 'xchk_tmux_content/status_line_items.html'
    strat = Strategy(refusing_check=TrueCheck(),accepting_check=Negation(TrueCheck()))


class CommandPrefixView(ContentView):
    uid = 'xchk_tmux_content_command_prefix'
    title = 'command prefix'
    template = 'xchk_tmux_content/command_prefix.html'
    strat = Strategy(refusing_check=TrueCheck(),accepting_check=Negation(TrueCheck()))


class OverzichtWindowsEnSessiesView(ContentView):
    uid = 'xchk_tmux_content_overzicht_windows_en_sessies'
    title = 'overzicht windows en sessies'
    template = 'xchk_tmux_content/overzicht_windows_en_sessies.html'
    strat = Strategy(refusing_check=TrueCheck(),accepting_check=Negation(TrueCheck()))


class PairProgrammingView(ContentView):
    uid = 'xchk_tmux_content_pair_programming'
    title = 'pair programming'
    template = 'xchk_tmux_content/pair_programming.html'
    strat = Strategy(refusing_check=TrueCheck(),accepting_check=Negation(TrueCheck()))


class CopyModeKeyTableView(ContentView):
    uid = 'xchk_tmux_content_copy_mode_key_table'
    title = 'copy-mode key table'
    template = 'xchk_tmux_content/copy_mode_key_table.html'
    strat = Strategy(refusing_check=TrueCheck(),accepting_check=Negation(TrueCheck()))


class ConfiguratieKleurenView(ContentView):
    uid = 'xchk_tmux_content_configuratie_kleuren'
    title = 'configuratie kleuren'
    template = 'xchk_tmux_content/configuratie_kleuren.html'
    strat = Strategy(refusing_check=TrueCheck(),accepting_check=Negation(TrueCheck()))


class BufferDoorzoekenView(ContentView):
    uid = 'xchk_tmux_content_buffer_doorzoeken'
    title = 'buffer doorzoeken'
    template = 'xchk_tmux_content/buffer_doorzoeken.html'
    strat = Strategy(refusing_check=TrueCheck(),accepting_check=Negation(TrueCheck()))


class AlDanNietBestaandeSessieGebruikenView(ContentView):
    uid = 'xchk_tmux_content_al_dan_niet_bestaande_sessie_gebruiken'
    title = 'Al dan niet bestaande sessie gebruiken'
    template = 'xchk_tmux_content/al_dan_niet_bestaande_sessie_gebruiken.html'
    strat = Strategy(refusing_check=TrueCheck(),accepting_check=Negation(TrueCheck()))


class SubconfiguratiesConditioneelInladenView(ContentView):
    uid = 'xchk_tmux_content_subconfiguraties_conditioneel_inladen'
    title = 'subconfiguraties conditioneel inladen'
    template = 'xchk_tmux_content/subconfiguraties_conditioneel_inladen.html'
    strat = Strategy(refusing_check=TrueCheck(),accepting_check=Negation(TrueCheck()))


class TmuxPluginsView(ContentView):
    uid = 'xchk_tmux_content_tmux_plugins'
    title = 'tmux plugins'
    template = 'xchk_tmux_content/tmux_plugins.html'
    strat = Strategy(refusing_check=TrueCheck(),accepting_check=Negation(TrueCheck()))


class CommandModeActiverenView(ContentView):
    uid = 'xchk_tmux_content_command_mode_activeren'
    title = 'command mode activeren'
    template = 'xchk_tmux_content/command_mode_activeren.html'
    strat = Strategy(refusing_check=TrueCheck(),accepting_check=Negation(TrueCheck()))


class LosmakenVanEenSessieView(ContentView):
    uid = 'xchk_tmux_content_losmaken_van_een_sessie'
    title = 'losmaken van een sessie'
    template = 'xchk_tmux_content/losmaken_van_een_sessie.html'
    strat = Strategy(refusing_check=TrueCheck(),accepting_check=Negation(TrueCheck()))


class PairenMetVerschillendeAccountsView(ContentView):
    uid = 'xchk_tmux_content_pairen_met_verschillende_accounts'
    title = 'pairen met verschillende accounts'
    template = 'xchk_tmux_content/pairen_met_verschillende_accounts.html'
    strat = Strategy(refusing_check=TrueCheck(),accepting_check=Negation(TrueCheck()))


class BufferStackView(ContentView):
    uid = 'xchk_tmux_content_buffer_stack'
    title = 'buffer stack'
    template = 'xchk_tmux_content/buffer_stack.html'
    strat = Strategy(refusing_check=TrueCheck(),accepting_check=Negation(TrueCheck()))


class IngebouwdePaneLayoutsGebruikenView(ContentView):
    uid = 'xchk_tmux_content_ingebouwde_pane_layouts_gebruiken'
    title = 'ingebouwde pane layouts gebruiken'
    template = 'xchk_tmux_content/ingebouwde_pane_layouts_gebruiken.html'
    strat = Strategy(refusing_check=TrueCheck(),accepting_check=Negation(TrueCheck()))


class PanesVerplaatsenView(ContentView):
    uid = 'xchk_tmux_content_panes_verplaatsen'
    title = 'panes verplaatsen'
    template = 'xchk_tmux_content/panes_verplaatsen.html'
    strat = Strategy(refusing_check=TrueCheck(),accepting_check=Negation(TrueCheck()))


class CommandDelayView(ContentView):
    uid = 'xchk_tmux_content_command_delay'
    title = 'command delay'
    template = 'xchk_tmux_content/command_delay.html'
    strat = Strategy(refusing_check=TrueCheck(),accepting_check=Negation(TrueCheck()))


class CustomConfiguratiefileGebruikenView(ContentView):
    uid = 'xchk_tmux_content_custom_configuratiefile_gebruiken'
    title = 'custom configuratiefile gebruiken'
    template = 'xchk_tmux_content/custom_configuratiefile_gebruiken.html'
    strat = Strategy(refusing_check=TrueCheck(),accepting_check=Negation(TrueCheck()))


class VensterPaneView(ContentView):
    uid = 'xchk_tmux_content_venster_pane'
    title = 'venster -> pane'
    template = 'xchk_tmux_content/venster_pane.html'
    strat = Strategy(refusing_check=TrueCheck(),accepting_check=Negation(TrueCheck()))


class TmuxInstallerenView(ContentView):
    uid = 'xchk_tmux_content_tmux_installeren'
    title = 'tmux installeren'
    template = 'xchk_tmux_content/tmux_installeren.html'
    strat = Strategy(refusing_check=TrueCheck(),accepting_check=Negation(TrueCheck()))


class WindowZoekenOpTitelView(ContentView):
    uid = 'xchk_tmux_content_window_zoeken_op_titel'
    title = 'window zoeken op titel'
    template = 'xchk_tmux_content/window_zoeken_op_titel.html'
    strat = Strategy(refusing_check=TrueCheck(),accepting_check=Negation(TrueCheck()))


class PanesMakenEnNavigerenView(ContentView):
    uid = 'xchk_tmux_content_panes_maken_en_navigeren'
    title = 'panes maken en navigeren'
    template = 'xchk_tmux_content/panes_maken_en_navigeren.html'
    strat = Strategy(refusing_check=TrueCheck(),accepting_check=Negation(TrueCheck()))


class TmuxConfigurerenView(ContentView):
    uid = 'xchk_tmux_content_tmux_configureren'
    title = 'tmux configureren'
    template = 'xchk_tmux_content/tmux_configureren.html'
    strat = Strategy(refusing_check=TrueCheck(),accepting_check=Negation(TrueCheck()))


class HooksView(ContentView):
    uid = 'xchk_tmux_content_hooks'
    title = 'hooks'
    template = 'xchk_tmux_content/hooks.html'
    strat = Strategy(refusing_check=TrueCheck(),accepting_check=Negation(TrueCheck()))


class NavigerenTussenSessiesView(ContentView):
    uid = 'xchk_tmux_content_navigeren_tussen_sessies'
    title = 'navigeren tussen sessies'
    template = 'xchk_tmux_content/navigeren_tussen_sessies.html'
    strat = Strategy(refusing_check=TrueCheck(),accepting_check=Negation(TrueCheck()))


class VenstersOfPanesMetEenCommandoView(ContentView):
    uid = 'xchk_tmux_content_vensters_of_panes_met_een_commando'
    title = 'vensters of panes met een commando'
    template = 'xchk_tmux_content/vensters_of_panes_met_een_commando.html'
    strat = Strategy(refusing_check=TrueCheck(),accepting_check=Negation(TrueCheck()))


class OptiesDefaultShortcutsBekijkenView(ContentView):
    uid = 'xchk_tmux_content_opties_default_shortcuts_bekijken'
    title = 'opties, default shortcuts,... bekijken'
    template = 'xchk_tmux_content/opties_default_shortcuts_bekijken.html'
    strat = Strategy(refusing_check=TrueCheck(),accepting_check=Negation(TrueCheck()))


class WatIsTmuxView(ContentView):
    uid = 'xchk_tmux_content_wat_is_tmux'
    title = 'Wat is tmux?'
    template = 'xchk_tmux_content/wat_is_tmux.html'
    strat = Strategy(refusing_check=TrueCheck(),accepting_check=Negation(TrueCheck()))


class EenVolledigPaneKopierenView(ContentView):
    uid = 'xchk_tmux_content_een_volledig_pane_kopieren'
    title = 'een volledig pane kopiëren'
    template = 'xchk_tmux_content/een_volledig_pane_kopieren.html'
    strat = Strategy(refusing_check=TrueCheck(),accepting_check=Negation(TrueCheck()))


class BeeindigenVanEenBestaandeSessieView(ContentView):
    uid = 'xchk_tmux_content_beeindigen_van_een_bestaande_sessie'
    title = 'beëindigen van een bestaande sessie'
    template = 'xchk_tmux_content/beeindigen_van_een_bestaande_sessie.html'
    strat = Strategy(refusing_check=TrueCheck(),accepting_check=Negation(TrueCheck()))


class IndexenVoorWindowsEnPanesInstellenView(ContentView):
    uid = 'xchk_tmux_content_indexen_voor_windows_en_panes_instellen'
    title = 'indexen voor windows en panes instellen'
    template = 'xchk_tmux_content/indexen_voor_windows_en_panes_instellen.html'
    strat = Strategy(refusing_check=TrueCheck(),accepting_check=Negation(TrueCheck()))


class PaneLoggenView(ContentView):
    uid = 'xchk_tmux_content_pane_loggen'
    title = 'pane loggen'
    template = 'xchk_tmux_content/pane_loggen.html'
    strat = Strategy(refusing_check=TrueCheck(),accepting_check=Negation(TrueCheck()))


class GroupedSessionsView(ContentView):
    uid = 'xchk_tmux_content_grouped_sessions'
    title = 'grouped sessions'
    template = 'xchk_tmux_content/grouped_sessions.html'
    strat = Strategy(refusing_check=TrueCheck(),accepting_check=Negation(TrueCheck()))


class PanesSluitenView(ContentView):
    uid = 'xchk_tmux_content_panes_sluiten'
    title = 'panes sluiten'
    template = 'xchk_tmux_content/panes_sluiten.html'
    strat = Strategy(refusing_check=TrueCheck(),accepting_check=Negation(TrueCheck()))


class KeyTablesView(ContentView):
    uid = 'xchk_tmux_content_key_tables'
    title = 'key tables'
    template = 'xchk_tmux_content/key_tables.html'
    strat = Strategy(refusing_check=TrueCheck(),accepting_check=Negation(TrueCheck()))


class TmuxCommandsUitvoerenBuitenEenSessieView(ContentView):
    uid = 'xchk_tmux_content_tmux_commands_uitvoeren_buiten_een_sessie'
    title = 'tmux commands uitvoeren buiten een sessie'
    template = 'xchk_tmux_content/tmux_commands_uitvoeren_buiten_een_sessie.html'
    strat = Strategy(refusing_check=TrueCheck(),accepting_check=Negation(TrueCheck()))


class CopyBufferOpslaanView(ContentView):
    uid = 'xchk_tmux_content_copy_buffer_opslaan'
    title = 'copy buffer opslaan'
    template = 'xchk_tmux_content/copy_buffer_opslaan.html'
    strat = Strategy(refusing_check=TrueCheck(),accepting_check=Negation(TrueCheck()))


class TmateView(ContentView):
    uid = 'xchk_tmux_content_tmate'
    title = 'tmate'
    template = 'xchk_tmux_content/tmate.html'
    strat = Strategy(refusing_check=TrueCheck(),accepting_check=Negation(TrueCheck()))


class MouseModeView(ContentView):
    uid = 'xchk_tmux_content_mouse_mode'
    title = 'mouse mode'
    template = 'xchk_tmux_content/mouse_mode.html'
    strat = Strategy(refusing_check=TrueCheck(),accepting_check=Negation(TrueCheck()))


class VenstersTussenSessiesVerplaatsenView(ContentView):
    uid = 'xchk_tmux_content_vensters_tussen_sessies_verplaatsen'
    title = 'vensters tussen sessies verplaatsen'
    template = 'xchk_tmux_content/vensters_tussen_sessies_verplaatsen.html'
    strat = Strategy(refusing_check=TrueCheck(),accepting_check=Negation(TrueCheck()))


class CommandInMeerderePanesUitvoerenView(ContentView):
    uid = 'xchk_tmux_content_command_in_meerdere_panes_uitvoeren'
    title = 'command in meerdere panes uitvoeren'
    template = 'xchk_tmux_content/command_in_meerdere_panes_uitvoeren.html'
    strat = Strategy(refusing_check=TrueCheck(),accepting_check=Negation(TrueCheck()))


class WindowsMakenNavigerenBasisSluitenView(ContentView):
    uid = 'xchk_tmux_content_windows_maken_navigeren_basis_sluiten'
    title = 'windows maken, navigeren (basis), sluiten'
    template = 'xchk_tmux_content/windows_maken_navigeren_basis_sluiten.html'
    strat = Strategy(refusing_check=TrueCheck(),accepting_check=Negation(TrueCheck()))


class SendCommandView(ContentView):
    uid = 'xchk_tmux_content_send_command'
    title = 'send command'
    template = 'xchk_tmux_content/send_command.html'
    strat = Strategy(refusing_check=TrueCheck(),accepting_check=Negation(TrueCheck()))


class VastmakenAanEenSessieView(ContentView):
    uid = 'xchk_tmux_content_vastmaken_aan_een_sessie'
    title = 'vastmaken aan een sessie'
    template = 'xchk_tmux_content/vastmaken_aan_een_sessie.html'
    strat = Strategy(refusing_check=TrueCheck(),accepting_check=Negation(TrueCheck()))


class PaneVensterView(ContentView):
    uid = 'xchk_tmux_content_pane_venster'
    title = 'pane -> venster'
    template = 'xchk_tmux_content/pane_venster.html'
    strat = Strategy(refusing_check=TrueCheck(),accepting_check=Negation(TrueCheck()))


class BasisPairProgrammingView(ContentView):
    uid = 'xchk_tmux_content_basis_pair_programming'
    title = 'basis pair programming'
    template = 'xchk_tmux_content/basis_pair_programming.html'
    strat = Strategy(refusing_check=TrueCheck(),accepting_check=Negation(TrueCheck()))
