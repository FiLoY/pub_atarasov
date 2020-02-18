<template>
    <div id="main">
        <navbar/>
        <div class="container">
            <transition name="fade" mode="out-in">
                <router-view/>
            </transition>
        </div>
    </div>
</template>

<script>
// @ is an alias to /src
import navbar from '@/components/navbar'

export default {
    name: 'main',
    components: {
        navbar,
    },
    watch: {
      '$route' (to, from) {
        document.title = to.meta.title || 'Your Website'
      },

    },
}
</script>
<style lang="scss">
#main {
    font-family: 'Avenir', Helvetica, Arial, sans-serif;
    -webkit-font-smoothing: antialiased;
    -moz-osx-font-smoothing: grayscale;
    color: #2c3e50;
}
#main .btn-primary {
    background-color: #854ed2;
    border: 1px solid transparent;
    transition: 0.6s ease;
}

#main .btn-primary:hover {
    background-color: white ;
    border: 1px solid #854ed2 ;
    color: #854ed2 ;
    transition: 0.6s ease ;
}

#main .btn-primary:focus, #main .btn-primary:active, #main .btn-primary:target {
    background-color: #854ed2;
    border: 1px solid transparent;
    transition: 0.6s ease;
    color: white;
}

#main input:focus, #main textarea:focus {
    border-color: #854ed2;
    transition: 0.6s ease;
}



.fade-enter-active,
.fade-leave-active {
  transition-duration: 0.3s;
  transition-property: opacity;
  transition-timing-function: ease;
}

.fade-enter,
.fade-leave-active {
  opacity: 0
}


</style>
