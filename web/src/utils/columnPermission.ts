import { useColumnPermission } from '/@/stores/columnPermission';

type permissionType = 'is_create' | 'is_query' | 'is_update';

export const columnPermission = (key: string, type: permissionType): boolean => {
	const permissions = useColumnPermission().permission || [];

	return !!permissions.some((i) => i.field_name === key && i[type]);
};
