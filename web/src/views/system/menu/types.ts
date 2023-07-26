export interface TreeTypes {
  id: number;
  name: string;
  status: boolean;
  children?: TreeTypes[];
}

export interface APIResponseData {
  code?: number;
  data: [];
  msg?: string;
}

export interface FormTypes<T> {
  [key: string]: T;
}

export interface ComponentFileItem {
  value: string;
  label: string;
}