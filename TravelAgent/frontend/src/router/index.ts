import {
    createRouter,
    createWebHistory
} from 'vue-router'

import PlannerView from '../views/PlannerView.vue'
import ResultView from '../views/ResultView.vue'

const router = createRouter({
    history: createWebHistory(),

    routes: [
        {
            path: '/',
            name: 'planner',
            component: PlannerView
        },
        {
            path: '/results/:resultId',
            name: 'result',
            component: ResultView,
            props: true
        }
    ]
})

export default router