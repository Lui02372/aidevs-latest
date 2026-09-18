"""Offline launcher checks; Docker, AWS and API keys are not used."""
import json
import os
from pathlib import Path
import shutil
import subprocess
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[1]
POWERSHELL = shutil.which('pwsh') or shutil.which('powershell')


@unittest.skipUnless(POWERSHELL and os.name == 'nt', 'Windows PowerShell required')
class LauncherTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory(prefix='runtime launcher ')
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        shutil.copy2(ROOT / 'launcher.ps1', self.root)
        self.project = self.root / 'project with spaces'
        self.project.mkdir()
        for name in ('infrastructure.yml', 'application.yml', 'guide.md'):
            (self.project / name).write_text('fixture', encoding='utf-8')
        (self.project / '.env.example').write_text('TEST_VALUE=example\n', encoding='utf-8')
        self.config = {'version': 1, 'targets': [{
            'id': '07', 'directory': self.project.name, 'title': 'Fixture',
            'guide': self.project.name + '/guide.md',
            'envExample': self.project.name + '/.env.example',
            'compose': ['infrastructure.yml', 'application.yml'],
            'pythonGroup': 'weather', 'url': 'http://localhost:8501',
            'services': ['frontend', 'backend'],
        }]}
        self.save_config()
        self.log = self.root / 'docker-calls.txt'
        (self.root / 'docker.cmd').write_text(
            '@echo off\n'
            'echo %CD%^|%*>>"%LAUNCHER_TEST_LOG%"\n'
            'if "%FAIL_COMPOSE%"=="1" if "%1"=="compose" exit /b 9\n'
            'exit /b 0\n', encoding='ascii')

    def save_config(self):
        (self.root / 'launcher.json').write_text(json.dumps(self.config), encoding='utf-8')

    def run_launcher(self, *args, fail=False):
        env = os.environ.copy()
        env['PATH'] = str(self.root) + os.pathsep + env['PATH']
        env['LAUNCHER_TEST_LOG'] = str(self.log)
        env['FAIL_COMPOSE'] = '1' if fail else '0'
        return subprocess.run(
            [POWERSHELL, '-NoProfile', '-File', str(self.root / 'launcher.ps1'),
             '-Target', '07', *args], cwd=self.root.parent, env=env,
            capture_output=True, text=True, encoding='utf-8', errors='replace', timeout=30)

    def test_init_preserves_existing_env(self):
        result = self.run_launcher('-Action', 'init')
        self.assertEqual(result.returncode, 0, result.stderr)
        target = self.project / '.env'
        self.assertEqual(target.read_text(encoding='utf-8'), 'TEST_VALUE=example\n')
        target.write_text('DO_NOT_REPLACE=1', encoding='utf-8')
        self.assertEqual(self.run_launcher('-Action', 'init').returncode, 0)
        self.assertEqual(target.read_text(), 'DO_NOT_REPLACE=1')

    def test_dry_run_has_no_side_effects(self):
        self.assertEqual(self.run_launcher('-Action', 'init', '-DryRun').returncode, 0)
        self.assertEqual(self.run_launcher('-Action', 'start', '-DryRun').returncode, 0)
        self.assertFalse((self.project / '.env').exists())
        self.assertFalse(self.log.exists())

    def test_start_and_stop_order(self):
        self.assertEqual(self.run_launcher('-Action', 'start').returncode, 0)
        commands = [line for line in self.log.read_text().splitlines() if ' up ' in line]
        self.assertIn('infrastructure.yml up', commands[0])
        self.assertIn('application.yml up', commands[1])
        self.assertTrue((self.project / '.env').exists())
        self.log.write_text('')
        self.assertEqual(self.run_launcher('-Action', 'stop').returncode, 0)
        commands = self.log.read_text().splitlines()
        self.assertIn('application.yml stop', commands[1])
        self.assertIn('infrastructure.yml stop', commands[2])

    def test_failure_stops_next_compose(self):
        self.assertNotEqual(self.run_launcher('-Action', 'start', fail=True).returncode, 0)
        calls = self.log.read_text()
        self.assertIn('infrastructure.yml', calls)
        self.assertNotIn('application.yml', calls)

    def test_path_escape_rejected(self):
        self.config['targets'][0]['directory'] = '../outside'
        self.save_config()
        self.assertNotEqual(self.run_launcher('-Action', 'start', '-DryRun').returncode, 0)

    def test_switch_stops_other_app_before_starting_selected(self):
        other = self.root / 'other app'
        shutil.copytree(self.project, other)
        item = dict(self.config['targets'][0], id='05', directory=other.name)
        self.config['targets'].append(item)
        self.save_config()
        result = self.run_launcher('-Action', 'switch')
        self.assertEqual(result.returncode, 0, result.stderr)
        calls = self.log.read_text().splitlines()
        stopped = [i for i, line in enumerate(calls) if ' stop' in line]
        started = [i for i, line in enumerate(calls) if ' up ' in line]
        self.assertEqual(len(stopped), 2)
        self.assertEqual(len(started), 2)
        self.assertLess(max(stopped), min(started))
        self.assertTrue(all('other app' in calls[i] for i in stopped))
        self.assertFalse(any('down' in line for line in calls))

    def test_switch_validation_failure_does_not_stop_existing_app(self):
        result = self.run_launcher('-Action', 'switch', fail=True)
        self.assertNotEqual(result.returncode, 0)
        calls = self.log.read_text()
        self.assertNotIn(' stop', calls)
        self.assertNotIn(' up ', calls)

    def test_open_dry_run_does_not_invoke_docker(self):
        result = self.run_launcher('-Action', 'open', '-DryRun')
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertIn('http://localhost:8501', result.stdout)
        self.assertFalse(self.log.exists())


class ManifestTests(unittest.TestCase):
    def test_all_manifest_files_exist(self):
        config = json.loads((ROOT / 'launcher.json').read_text(encoding='utf-8-sig'))
        ids = [item['id'] for item in config['targets']]
        self.assertEqual(len(ids), len(set(ids)))
        self.assertEqual(set(ids), {'00', '01', '01-2', '01-3', '02', '03', '04', '05', '06', '07'})
        for item in config['targets']:
            self.assertIsInstance(item['services'], list)
            self.assertTrue((ROOT / item['guide']).is_file(), item['guide'])
            for filename in item['compose']:
                self.assertTrue((ROOT / item['directory'] / filename).is_file())
            if item['compose']:
                self.assertTrue((ROOT / item['envExample']).is_file())
            self.assertTrue((ROOT / item['directory'] / 'launcher.cmd').is_file())
            if item['url']:
                self.assertIn('backend', item['services'])
                self.assertIn('frontend', item['services'])


if __name__ == '__main__':
    unittest.main()
