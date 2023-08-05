import boto3

class CloudFormation:
  def __init__(self, region="eu-west-2", stack_name_separator="-"):
    self._region = region
    self._stack_name_separator = stack_name_separator

  @property
  def cf_client(self):
    if not hasattr(self, "_cf_client"):
      self._cf_client = boto3.client('cloudformation', region_name=self._region)
    return self._cf_client

  def get_exports(self, stack_prefix, stack_name=None):
    paginator = self.cf_client.get_paginator('list_exports')
    page_iterator = paginator.paginate()
    exports = []
    for page in page_iterator:
      exports = exports + page['Exports']

    exports = [export for export in exports if export['Name'].startswith(self.get_stack_prefix(stack_prefix, stack_name))]

    return exports

  def get_stack_prefix(self, stack_prefix, stack_name=None):
    stack_prefixes = [stack_prefix]
    if stack_name:
      stack_prefixes.append(stack_name)
    stack_prefixes.append("")
    return self._stack_name_separator.join(stack_prefixes)


  def exports_to_parameters(self, stack_prefix, stack_name=None):
    parameters = []
    for export in self.get_exports(stack_prefix, stack_name):
      parameter_name = export['Name'].replace(self.get_stack_prefix(stack_prefix, stack_name), "")
      if not stack_name:
        parameter_name = "-".join(parameter_name.split("-")[1:])
      parameters.append({
        "Name": parameter_name,
        "Value": export["Value"]
      })

    return parameters
