export interface TreeType {
  id: number;
  name: string;
  status: boolean;
  children?: TreeType[];
}

export interface APIResponseData {
  code?: number;
  data: [];
  msg?: string;
}

export interface FormType<T> {
  [key: string]: T;
}

export interface TreeItemType {
  id?: number;
  modifier_name?: string;
  creator_name?: string;
  create_datetime?: string;
  update_datetime?: string;
  parent_name?: string;
  status_label?: string;
  has_children?: number;
  hasChild?: false,
  description?: string;
  modifier?: string;
  dept_belong_id?: string;
  name?: string;
  key?: string;
  sort?: number;
  owner?: string;
  phone?: string;
  email?: string;
  status?: boolean;
  creator?: number;
  parent?: number;
}

export interface DeptFormDataType {
  id: string;
  key: string;
  parent: string;
  name: string;
  owner: string;
  phone: string;
  email: string;
  sort: number;
  is_catalog?: boolean;
}