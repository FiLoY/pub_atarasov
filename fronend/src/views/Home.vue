<template>
    <div class="home">
            <h1>Привет</h1>

        <p>
                <button @click="decrement">-</button>

            {{ count }}
    <button @click="increment">+</button>

        </p>
    </div>
</template>

<script>
// @ is an alias to /src
export default {
    name: 'home',
    components: {
    },
    computed: {
        count() {
            return this.$store.state.count
        }
    },
    methods: {
        increment() {
            console.log('нажал +')
            this.$store.commit('increment')
        },
                decrement() {
            console.log('нажал -')
            this.$store.commit('decrement')
        }
    }

}
</script>
