from platform_agent.cmd.wg_info import WireGuardRead

import mock


@mock.patch('platform_agent.cmd.wg_info.os.popen')
def test_wireguard_read(patch_cmd_read, mock_wg_show, wg_show_dict):
    patch_cmd_read().read.return_value = mock_wg_show
    wg = WireGuardRead()
    wg_info = wg.wg_info()
    assert wg_info == wg_show_dict
