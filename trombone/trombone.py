import json
import subprocess
from typing import Dict, List, Optional, Tuple


class Trombone:

    def __init__(self, jar_path: str):
        self.jar_path = jar_path

    def run(self, key_values: Optional[List[Tuple[str, str]]] = None) -> Tuple[str, str]:
        formatted_args = []
        if key_values:
            formatted_args = [f'{key}={value}' for key, value in key_values]

        process = subprocess.Popen(
            ['java', '-jar', self.jar_path] + formatted_args,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE
        )

        stdout, stderr = process.communicate()

        return stdout.decode(), stderr.decode()

    def serialize_output(self, output: str) -> Dict:
        index_where_json_start = 0

        for i, c in enumerate(output):
            if c == '{':
                index_where_json_start = i
                break

        return json.loads(output[index_where_json_start:])
