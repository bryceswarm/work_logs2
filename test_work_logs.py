from unittest import main, TestCase, mock

from work_logs import clear_screen, new_task, _get_time_elapsed, \
                      menu_loop, search_menu_loop, display_task


class TestClearScreen(TestCase):
    @mock.patch('work_logs.os')
    def test_clear_screen(self, mock_os):
        mock_os.name = 'nt'
        clear_screen()
        mock_os.system.assert_called_once_with('cls')

    @mock.patch('work_logs.os')
    def test_clear_screen_not_nt(self, mock_os):
        mock_os.name = 'bob'
        clear_screen()
        mock_os.system.assert_called_once_with('clear')


class TestNewTask(TestCase):
    @mock.patch('work_logs.Tasks.create')
    @mock.patch('work_logs.clear_screen')
    @mock.patch('builtins.input')
    def test_new_task(self, mock_input, mock_clear_screen, mock_create,):
        mock_input.side_effect = ['Bryce', 'Coding', '15', 'none', 'b']
        new_task()
        mock_create.assert_called_once_with(employee_name='Bryce',
                                            notes='none',
                                            task_name='Coding',
                                            time_elapsed='15')
        self.assertEqual(4, mock_clear_screen.call_count)


class TestElapsedTime(TestCase):
    @mock.patch('builtins.input')
    def test_elapsed_time(self, mock_input):
        mock_input.side_effect = ['n', '2']
        _get_time_elapsed()


class TestMenu(TestCase):
    @mock.patch('builtins.input', return_value='Q')
    def test_menu_loop(self, mock_input):
        self.assertRaises(SystemExit, menu_loop())

    @mock.patch('builtins.input', return_value='Q')
    def test_search_menu_loop(self, mock_input):
        self.assertRaises(SystemExit, search_menu_loop())


class TestDisplay(TestCase):
    @mock.patch('builtins.input', return_value='3')
    def test_display(self, mock_input):
        self.assertRaises(SystemExit, display_task())


if __name__ == '__main__':
    main()
