from os import path
import subprocess
THIS_FOLDER = path.abspath(path.dirname(__file__))

def ansible_staging_cmd(pattern, module, args):
    try:
        result = subprocess.check_output(
            [
                'ansible',
                pattern,
                '--inventory=../deploy_tools/ansible/hosts-staging',
                '--private-key=~/.ssh/id_rsa',
                '--module-name={}'.format(module),
                '--args={}'.format(args),
                '--user="{{ deployment_user }}"',
                '-vvvv',
            ],
            stderr=subprocess.STDOUT,
            cwd=THIS_FOLDER
        ).decode().strip()
    except subprocess.CalledProcessError as exc:
        print('>>>>>>>>>>>>>>>')
        print('Ansible Output:')
        print('---------------')
        print(exc.output.decode())
        print('<<<<<<<<<<<<<<<')
        raise
    assert result != 'No hosts matched', 'No hosts matched for Ansible command'
    return result


def create_session_on_server(host, email):
    return ansible_staging_cmd(
            pattern=host,
            module='command',
            args='{{ django_manage_cmd }} create_session %s' % (email,)
    )


def reset_database(host):
    return ansible_staging_cmd(
            pattern=host,
            module='command',
            args='{{ django_manage_cmd }} flush --noinput'
    )
