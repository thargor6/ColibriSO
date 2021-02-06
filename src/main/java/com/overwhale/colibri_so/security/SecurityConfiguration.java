package com.overwhale.colibri_so.security;

import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.context.annotation.Configuration;
import org.springframework.security.config.annotation.authentication.builders.AuthenticationManagerBuilder;
import org.springframework.security.config.annotation.web.builders.HttpSecurity;
import org.springframework.security.config.annotation.web.configuration.EnableWebSecurity;
import org.springframework.security.config.annotation.web.configuration.WebSecurityConfigurerAdapter;
import org.springframework.security.crypto.bcrypt.BCryptPasswordEncoder;
import org.springframework.security.crypto.password.PasswordEncoder;

import javax.sql.DataSource;

@EnableWebSecurity
@Configuration
public class SecurityConfiguration extends WebSecurityConfigurerAdapter {

  @Autowired
  private DataSource dataSource;

  @Override
  protected void configure(HttpSecurity http) throws Exception {
    // ignore csrf for login processing url and Vaadin endpoint requests
    http.csrf().ignoringAntMatchers("/login", "/connect/**");

    // Vaadin renders a client-side login page at "/login" (see the routes
    // config in index.ts).
    //
    // This configures Spring Security to
    //     (i) listen for form login HTTP POST requests on "/login"
    //         This is actually used by the client-side login form.
    //         In this app the login form is built assuming the Spring Security
    //         defaults: parameter names, form data submission, handler URL,
    //         success and failure responses. If any of that changes (either
    //         in the Spring Security config here, or in the client-side login
    //         form, the other part should be updated accordingly.
    //    (ii) ignore HTTP GET requests to "/login"
    //         (i.e. do not render the default Spring Security login form)
    //         The `/login` HTTP GET is handled in the same way as any
    //         other HTTP GET: the app shell is returned and routing happens
    //         on the client side.
    //   (iii) redirect unauthenticated HTTP GET requests to "/login"
    //         This is used only if Spring Security is actually configured
    //         to require authentication for some HTTP requests.
    //         In this app this may be irrelevant because it's OK to allow
    //         _all_ HTTP GET requests and let the client-side redirect to
    //         /login when necessary.
    http.formLogin().loginPage("/login");

    // Spring Security supports logout requests by default, so there is no need
    // to configure it separately. However, it's important that it's configured
    // because this app assumes the default `/logout` HTTP GET handler.
    // http.logout();
  }

  @Override
  protected void configure(AuthenticationManagerBuilder auth) throws Exception {
    // Configure users and roles in memory
    //auth.inMemoryAuthentication().withUser("user").password("{noop}password").roles("USER");
    auth.jdbcAuthentication()
            .dataSource(dataSource)
            .passwordEncoder(passwordEncoder())
            .usersByUsernameQuery("select USERNAME,PASSWORD_HASH PASSWORD, ENABLED "
                    + "from USERS "
                    + "where USERNAME = ?")
            .authoritiesByUsernameQuery("select USERNAME, AUTHORITY "
                    + "from USER_AUTHORITIES, USERS, AUTHORITIES "
                    + "where USERNAME = ? "
                    + "and USERS.ID = USER_ID "
                    + "and AUTHORITIES.ID = AUTHORITY_ID");
  }

  public PasswordEncoder passwordEncoder() {
    return new BCryptPasswordEncoder();
  }
}
