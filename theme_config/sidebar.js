import { csSidebar } from './sidebar/cs'
import { javaSidebar } from './sidebar/java'
import { databaseSidebar } from './sidebar/database'
import { frameworkSidebar } from './sidebar/framework'
import { distributedSidebar } from './sidebar/distributed'
import { designSidebar } from './sidebar/design'
import { questionsSidebar } from './sidebar/questions'
import { interviewPrepSidebar } from './sidebar/interview-prep'

export const sidebar = {
  '/interview-prep/': interviewPrepSidebar,
  '/cs/': csSidebar,
  '/java/': javaSidebar,
  '/database/': databaseSidebar,
  '/framework/': frameworkSidebar,
  '/distributed/': distributedSidebar,
  '/design/': designSidebar,
  '/questions/': questionsSidebar,
}
