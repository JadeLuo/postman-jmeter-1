import json
import os
import sys
import warnings
import xmltodict


def get_postman(path):
    with open(path, 'r', encoding='UTF-8') as postman_f:
        result_dict = json.load(postman_f)
        return result_dict


def generate_jmeter(name, body):
    shell = {
        'jmeterTestPlan': {
            '@version': '1.2',
            '@properties': '4.0',
            '@jmeter': '4.0 r1823414',
            'hashTree': {
                'TestPlan': {
                    '@guiclass': 'TestPlanGui',
                    '@testclass': 'TestPlan',
                    '@testname': name,
                    '@enabled': 'true',
                    'stringProp': [
                        {
                            '@name': 'TestPlan.comments'
                        },
                        {
                            '@name': 'TestPlan.user_define_classpath'
                        }
                    ],
                    'boolProp': [
                        {
                            '@name': 'TestPlan.functional_mode',
                            '#text': 'false'
                        },
                        {
                            '@name': 'TestPlan.tearDown_on_shutdown',
                            '#text': 'true'
                        },
                        {
                            '@name': 'TestPlan.serialize_threadgroups',
                            '#text': 'false'
                        }
                    ],
                    'elementProp': {
                        '@name': 'TestPlan.user_defined_variables',
                        '@elementType': 'Arguments',
                        '@guiclass': 'ArgumentsPanel',
                        '@testclass': 'Arguments',
                        '@testname': '用户定义的变量',
                        '@enabled': 'true',
                        'collectionProp': {
                            '@name': 'Arguments.arguments',
                            'elementProp': [
                                {
                                    '@name': 'host',
                                    '@elementType': 'Argument',
                                    'stringProp': [
                                        {
                                            '@name': 'Argument.name',
                                            '#text': 'host'
                                        },
                                        { '@name': 'Argument.value' },
                                        {
                                            '@name': 'Argument.metadata',
                                            '#text': '='
                                        }
                                    ]
                                },
                                {
                                    '@name': 'protocol',
                                    '@elementType': 'Argument',
                                    'stringProp': [
                                        {
                                            '@name': 'Argument.name',
                                            '#text': 'protocol'
                                        },
                                        {
                                            '@name': 'Argument.value',
                                            '#text': 'http'
                                        },
                                        {
                                            '@name': 'Argument.metadata',
                                            '#text': '='
                                        }
                                    ]
                                },
                                {
                                    '@name': 'port',
                                    '@elementType': 'Argument',
                                    'stringProp': [
                                        {
                                            '@name': 'Argument.name',
                                            '#text': 'port'
                                        },
                                        {
                                            '@name': 'Argument.value',
                                            '#text': '80'
                                        },
                                        {
                                            '@name': 'Argument.metadata',
                                            '#text': '='
                                        }
                                    ]
                                }
                            ]
                        }
                    }
                },
                'hashTree': {
                    'ThreadGroup': {
                        '@guiclass': 'ThreadGroupGui',
                        '@testclass': 'ThreadGroup',
                        '@testname': '线程组',
                        '@enabled': 'true',
                        'stringProp': [
                            {
                                '@name': 'ThreadGroup.on_sample_error',
                                '#text': 'continue'
                            },
                            {
                                '@name': 'ThreadGroup.num_threads',
                                '#text': '1'
                            },
                            {
                                '@name': 'ThreadGroup.ramp_time',
                                '#text': '1'
                            },
                            {
                                '@name': 'ThreadGroup.duration'
                            },
                            {
                                '@name': 'ThreadGroup.delay'
                            }
                        ],
                        'elementProp': {
                            '@name': 'ThreadGroup.main_controller',
                            '@elementType': 'LoopController',
                            '@guiclass': 'LoopControlPanel',
                            '@testclass': 'LoopController',
                            '@testname': '循环控制器',
                            '@enabled': 'true',
                            'boolProp': {
                                '@name': 'LoopController.continue_forever',
                                '#text': 'false'
                            },
                            'stringProp': {
                                '@name': 'LoopController.loops',
                                '#text': '1'
                            }
                        },
                        'boolProp': {
                            '@name': 'ThreadGroup.scheduler',
                            '#text': 'false'
                        }
                    },
                    'hashTree': {
                        'HTTPSamplerProxy': [
                        ]
                    }
                }
            }
        }
    }
    body_path = shell['jmeterTestPlan']['hashTree']['hashTree']['hashTree']['HTTPSamplerProxy']
    for item in body:
        body_path.append(item)
    if os.path.exists(name+'.jmx'):
        os.remove(name+'.jmx')
    f = open(name+'.jmx', 'a+', encoding='UTF-8')
    converted_xml = xmltodict.unparse(shell, encoding='UTF-8', pretty=True)
    converted_xml = converted_xml.replace('</HTTPSamplerProxy>', '</HTTPSamplerProxy>\n                <hashTree/>')
    f.write(converted_xml)
    f.close()


def postman2jmeter(postman_dict):
    body = []
    project = postman_dict['info']['name']  # 项目名称
    for directory in postman_dict['item']:
        dir_name = directory['name']  # 文件夹名称
        for request in directory['item']:
            request_body = {
                '@guiclass': 'HttpTestSampleGui',
                '@testclass': 'HTTPSamplerProxy',
                '@testname': '',
                '@enabled': 'true',
                'elementProp': [{
                    '@name': 'HTTPsampler.Arguments',
                    '@elementType': 'Arguments',
                    '@guiclass': 'HTTPArgumentsPanel',
                    '@testclass': 'Arguments',
                    '@testname': '用户定义的变量',
                    '@enabled': 'true',
                    'collectionProp': {
                        '@name': 'Arguments.arguments',
                        'elementProp': [
                        ]
                    }
                }, {
                    '@name': 'HTTPsampler.Files',
                    '@elementType': 'HTTPFileArgs',
                    'collectionProp': {
                        '@name': 'HTTPFileArgs.files',
                        'elementProp': [
                        ]
                    }
                }],
                'stringProp': [
                ],
                'boolProp': [
                ]
            }
            request_name = '[' + dir_name + ']' + request['name']  # 接口名称
            request_body['@testname'] = request_name
            request_body['stringProp'].append({
                '@name': 'HTTPSampler.method',
                '#text': request['request']['method']
            })
            request_body['stringProp'].append({
                "@name": "HTTPSampler.domain",
                "#text": '${host}'
            })
            request_body['stringProp'].append({
                "@name": "HTTPSampler.port",
                "#text": '${port}'
            })
            request_body['stringProp'].append({
                "@name": "HTTPSampler.protocol",
                "#text": '${protocol}'
            })
            request_body['stringProp'].append({
                "@name": "HTTPSampler.contentEncoding",
                "#text": "UTF-8"
            })
            try:
                url_params_path = request_body['elementProp'][0]['collectionProp']['elementProp']
                body_params_path = request_body['elementProp'][1]['collectionProp']['elementProp']
                request_body['stringProp'].append({
                    "@name": "HTTPSampler.path",
                    "#text": '/'.join(request['request']['url']['path'])
                })
                if 'query' in request['request']['url']:
                    url_params = request['request']['url']['query']
                    for param in url_params:
                        url_params_path.append({
                            "@name": "key",
                            "@elementType": "HTTPArgument",
                            "boolProp": [
                                {
                                    "@name": "HTTPArgument.always_encode",
                                    "#text": "false"
                                },
                                {
                                    "@name": "HTTPArgument.use_equals",
                                    "#text": "true"
                                }
                            ],
                            "stringProp": [
                                {
                                    "@name": "Argument.value",
                                    "#text": param['value']
                                },
                                {
                                    "@name": "Argument.metadata",
                                    "#text": "="
                                },
                                {
                                    "@name": "Argument.name",
                                    "#text": param['key']
                                }
                            ]
                        })
                body_mode = request['request']['body']['mode']
                if body_mode == 'formdata':
                    body_params = request['request']['body']['formdata']
                    for param in body_params:
                        if param['type'] == 'file':
                            body_params_path.append({
                                "@name": "key",
                                "@elementType": "HTTPFileArg",
                                "stringProp": [
                                    {
                                        "@name": "File.path",
                                        "#text": param['src']
                                    },
                                    {
                                        "@name": "File.paramname",
                                        "#text": param['key']
                                    },
                                    {
                                        "@name": "File.mimetype",
                                        "#text": "application/octet-stream"
                                    }
                                ]
                            })
                body.append(request_body)
            except KeyError:
                # print(request)

                warning_msg = request_name+' => 参数出现问题！'
                warnings.showwarning(warning_msg, UserWarning, '', '')
                warnings.showwarning(request, IndexError, '', '')
            # print(request)
    return project, body


if __name__ == "__main__":
    if len(sys.argv) == 1:
        print("Type your filename as first parameter please.")
        exit(-1)
    postman_json = get_postman(sys.argv[1])
    project_name, jmeter_body = postman2jmeter(postman_json)
    generate_jmeter(project_name, jmeter_body)
