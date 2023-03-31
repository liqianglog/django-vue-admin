import permissionDirective from './directive.permission'
import permissionFunc from './func.permission'
const install = function (app:any) {
  app.directive('permission', permissionDirective)
  app.provide('$hasPermissions',permissionFunc.hasPermissions)
}

export default {
  install
}
