import { csSidebar } from './sidebar/cs'
import { databaseSidebar } from './sidebar/database'
import { devopsSidebar } from './sidebar/devops'
import { distributedSidebar } from './sidebar/distributed'
import { frameworkSidebar } from './sidebar/framework'
import { highThroughputSidebar } from './sidebar/high-throughput'
import { interviewSidebar } from './sidebar/interview'
import { javaSidebar } from './sidebar/java'
import { middlewareSidebar } from './sidebar/middleware'

export const sidebar = {
  '/cs/': csSidebar,
  '/database/': databaseSidebar,
  '/devops': devopsSidebar,
  '/distributed/': distributedSidebar,
  '/framework/': frameworkSidebar,
  '/high-throughput/': highThroughputSidebar,
  '/interview/': interviewSidebar,
  '/java/': javaSidebar,
  '/middleware/': middlewareSidebar,
}
