import { Package, ShoppingCart, Users, TrendingUp, AlertTriangle, CheckCircle } from 'lucide-react'

const stats = [
  { name: 'Total Items', value: '1,234', icon: Package, change: '+12%', changeType: 'positive' },
  { name: 'Active Orders', value: '45', icon: ShoppingCart, change: '+8%', changeType: 'positive' },
  { name: 'Suppliers', value: '23', icon: Users, change: '+2%', changeType: 'positive' },
  { name: 'Low Stock Items', value: '7', icon: AlertTriangle, change: '-3%', changeType: 'negative' },
]

const recentActivities = [
  { id: 1, action: 'New order created', item: 'Order #1234', time: '2 minutes ago', type: 'order' },
  { id: 2, action: 'Stock updated', item: 'Widget A - 50 units', time: '15 minutes ago', type: 'inventory' },
  { id: 3, action: 'New supplier added', item: 'ABC Corp', time: '1 hour ago', type: 'supplier' },
  { id: 4, action: 'Low stock alert', item: 'Widget B - 5 units left', time: '2 hours ago', type: 'alert' },
]

export const DashboardPage = () => {
  return (
    <div className="space-y-6">
      <div>
        <h1 className="text-2xl font-bold text-gray-900">Dashboard</h1>
        <p className="mt-1 text-sm text-gray-500">
          Overview of your inventory management system
        </p>
      </div>

      {/* Stats Grid */}
      <div className="grid grid-cols-1 gap-5 sm:grid-cols-2 lg:grid-cols-4">
        {stats.map((stat) => (
          <div key={stat.name} className="bg-white overflow-hidden shadow rounded-lg">
            <div className="p-5">
              <div className="flex items-center">
                <div className="flex-shrink-0">
                  <stat.icon className="h-6 w-6 text-gray-400" aria-hidden="true" />
                </div>
                <div className="ml-5 w-0 flex-1">
                  <dl>
                    <dt className="text-sm font-medium text-gray-500 truncate">
                      {stat.name}
                    </dt>
                    <dd className="flex items-baseline">
                      <div className="text-2xl font-semibold text-gray-900">
                        {stat.value}
                      </div>
                      <div className={`ml-2 flex items-baseline text-sm font-semibold ${
                        stat.changeType === 'positive' ? 'text-green-600' : 'text-red-600'
                      }`}>
                        {stat.change}
                      </div>
                    </dd>
                  </dl>
                </div>
              </div>
            </div>
          </div>
        ))}
      </div>

      <div className="grid grid-cols-1 gap-6 lg:grid-cols-2">
        {/* Recent Activities */}
        <div className="bg-white shadow rounded-lg">
          <div className="px-4 py-5 sm:p-6">
            <h3 className="text-lg leading-6 font-medium text-gray-900">
              Recent Activities
            </h3>
            <div className="mt-5">
              <div className="flow-root">
                <ul className="-mb-8">
                  {recentActivities.map((activity, activityIdx) => (
                    <li key={activity.id}>
                      <div className="relative pb-8">
                        {activityIdx !== recentActivities.length - 1 ? (
                          <span
                            className="absolute top-4 left-4 -ml-px h-full w-0.5 bg-gray-200"
                            aria-hidden="true"
                          />
                        ) : null}
                        <div className="relative flex space-x-3">
                          <div>
                            <span className={`h-8 w-8 rounded-full flex items-center justify-center ring-8 ring-white ${
                              activity.type === 'alert' ? 'bg-red-500' :
                              activity.type === 'order' ? 'bg-blue-500' :
                              activity.type === 'inventory' ? 'bg-green-500' :
                              'bg-gray-500'
                            }`}>
                              {activity.type === 'alert' ? (
                                <AlertTriangle className="h-4 w-4 text-white" />
                              ) : activity.type === 'order' ? (
                                <ShoppingCart className="h-4 w-4 text-white" />
                              ) : activity.type === 'inventory' ? (
                                <CheckCircle className="h-4 w-4 text-white" />
                              ) : (
                                <Package className="h-4 w-4 text-white" />
                              )}
                            </span>
                          </div>
                          <div className="min-w-0 flex-1 pt-1.5 flex justify-between space-x-4">
                            <div>
                              <p className="text-sm text-gray-500">
                                {activity.action} <span className="font-medium text-gray-900">{activity.item}</span>
                              </p>
                            </div>
                            <div className="text-right text-sm whitespace-nowrap text-gray-500">
                              {activity.time}
                            </div>
                          </div>
                        </div>
                      </div>
                    </li>
                  ))}
                </ul>
              </div>
            </div>
          </div>
        </div>

        {/* Quick Actions */}
        <div className="bg-white shadow rounded-lg">
          <div className="px-4 py-5 sm:p-6">
            <h3 className="text-lg leading-6 font-medium text-gray-900">
              Quick Actions
            </h3>
            <div className="mt-5 grid grid-cols-1 gap-3 sm:grid-cols-2">
              <button className="inline-flex items-center px-4 py-2 border border-transparent text-sm font-medium rounded-md shadow-sm text-white bg-primary-600 hover:bg-primary-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-primary-500">
                <Package className="h-4 w-4 mr-2" />
                Add Item
              </button>
              <button className="inline-flex items-center px-4 py-2 border border-transparent text-sm font-medium rounded-md shadow-sm text-white bg-green-600 hover:bg-green-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-green-500">
                <ShoppingCart className="h-4 w-4 mr-2" />
                New Order
              </button>
              <button className="inline-flex items-center px-4 py-2 border border-transparent text-sm font-medium rounded-md shadow-sm text-white bg-blue-600 hover:bg-blue-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-blue-500">
                <Users className="h-4 w-4 mr-2" />
                Add Supplier
              </button>
              <button className="inline-flex items-center px-4 py-2 border border-transparent text-sm font-medium rounded-md shadow-sm text-white bg-yellow-600 hover:bg-yellow-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-yellow-500">
                <TrendingUp className="h-4 w-4 mr-2" />
                View Reports
              </button>
            </div>
          </div>
        </div>
      </div>
    </div>
  )
}
