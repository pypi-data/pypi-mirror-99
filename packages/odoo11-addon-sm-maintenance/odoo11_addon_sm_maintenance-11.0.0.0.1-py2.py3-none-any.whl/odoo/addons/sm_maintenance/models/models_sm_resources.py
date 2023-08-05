def list_to_string(list):
  return ', '.join(str(e) for e in list)


def compute_name(action_name):
  # return "Action " + action_name + " has been done successfully"
  return action_name


class sm_resources:
  __instance = None
  successful_action_message_wizard = None

  @staticmethod
  def getInstance():
    if sm_resources.__instance is None:
      sm_resources()
    return sm_resources.__instance

  def __init__(self):
    if sm_resources.__instance is not None:
      raise Exception("This class is a singleton!")
    else:
      sm_resources.__instance = self

  def get_successful_action_message(self, parent, action_name, model_name):
    params = {
      'action': action_name,
      'model': model_name
    }

    name = compute_name(action_name)
    model_to_create = parent.env['sm_maintenance.successful_action_message'].create(params)
    vista = self.get_successful_message_id(parent)

    return {
      'type': 'ir.actions.act_window',
      'name': name,
      'res_model': 'sm_maintenance.successful_action_message',
      'view_type': 'form',
      'view_mode': 'form',
      'res_id': model_to_create.id,
      'view_id': vista,
      'target': 'new',
    }

  def get_successful_message_id(self, parent):
    saved_id = self.successful_action_message_wizard
    if saved_id is None:
      view_ref = parent.env['ir.ui.view'].search(
        [('name', '=', 'sm_maintenance.successful_action_message_wizard')])
      self.set_successful_message_view_id(view_ref.id)
      return view_ref.id
    return saved_id

  def set_successful_message_view_id(self, new_id):
    self.successful_action_message_wizard = new_id
