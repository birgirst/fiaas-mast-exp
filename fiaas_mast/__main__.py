
# Copyright 2017-2019 The FIAAS Authors
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

from fiaas_mast.app import create_app
import argparse
from .application_generator import ApplicationGenerator
from .configmap_generator import ConfigMapGenerator
from .common import make_safe_name
from .models import Release
import yaml
import json


parser = argparse.ArgumentParser()
parser.add_argument("--appspec", help="Generate application", default=None)
parser.add_argument("--configmap", help="Generate configmap", default=None)
parser.add_argument("--namespace", help="Namespace", default=None)
parser.add_argument("--image", help="Image", default=None)
parser.add_argument("--application-name", help="Application name", default=None)


yaml.SafeDumper.yaml_representers[None] = lambda self, data: \
    yaml.representer.SafeRepresenter.represent_str(
        self,
        str(data),
    )


def main():
    args = parser.parse_args()
    if args.appspec:
        with open(args.appspec,"r") as f:
            config_raw = yaml.safe_load(f.read())
        generator = ApplicationGenerator(None)
        deployment_id, application = generator.generate_application(
            args.namespace,
            Release(
                image=args.image,
                config_url=None,
                application_name=make_safe_name(args.application_name),
                original_application_name=args.application_name,
                spinnaker_tags={},
                raw_tags={},
                raw_labels={},
                metadata_annotations={},
                config_raw=config_raw))
        print(json.dumps({"deployment_id": deployment_id, "application": application}, default=lambda o: o.__dict__.get("_values") if "_values" in o.__dict__ else o.__dict__, indent=4))
    elif args.configmap:
        print("Generating configmap manifest")
    else:
        print("birgir")
        app = create_app()
        app.run(host="0.0.0.0", port=int(app.config['PORT']), debug=bool(app.config['DEBUG']))


if __name__ == '__main__':
    main()


