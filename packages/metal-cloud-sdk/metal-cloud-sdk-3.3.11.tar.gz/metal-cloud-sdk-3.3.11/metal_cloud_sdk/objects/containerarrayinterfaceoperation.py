# -*- coding: utf-8 -*-

class ContainerArrayInterfaceOperation(object):
	"""
	ContainerArrayInterfaceOperation contains information regarding the changes
	that are to be made to a product. Edit and deploy functions have to be
	called in order to apply the changes. The operation type and status are
	unique to each operation object.
	"""

	def __init__(self, container_array_interface_id, container_array_interface_change_id):
		self.container_array_interface_id = container_array_interface_id;
		self.container_array_interface_change_id = container_array_interface_change_id;


	"""
	The container_array_interface's label which is unique and it is used to form
	the <code>container_array_interface_subdomain</code>. Can be used to call
	API functions.
	"""
	container_array_interface_label = None;

	"""
	Automatically created based on <code>container_array_interface_label</code>.
	It is a unique reference to the ContainerArrayInterface object.
	"""
	container_array_interface_subdomain = None;

	"""
	The status of the deploy process.
	"""
	container_array_interface_deploy_status = None;

	"""
	The operation applied to ContainerArray interface.
	"""
	container_array_interface_deploy_type = None;

	"""
	The ID of the ContainerArray interface.
	"""
	container_array_interface_id = None;

	"""
	The ID of the ContainerArray that the interface belongs to.
	"""
	container_array_id = None;

	"""
	The ID of the network to which the ContainerArray interface is attached.
	"""
	network_id = None;

	"""
	ISO 8601 timestamp which holds the date and time when the ContainerArray
	interface was edited. Example format: 2013-11-29T13:00:01Z.
	"""
	container_array_interface_updated_timestamp = None;

	"""
	Shows the index of the interface. Numbering starts at 0. There are 2
	interfaces for ContainerArray, with indexes 0 and 1.
	"""
	container_array_interface_index = None;

	"""
	The schema type.
	"""
	type = None;

	"""
	This property helps ensure that edit operations don’t overwrite other,
	more recent changes made to the same object. It gets updated automatically
	after each successful edit operation.
	"""
	container_array_interface_change_id = None;
