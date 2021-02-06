package com.overwhale.colibri_so.domain.entity;

import lombok.Data;
import org.hibernate.annotations.Type;
import org.springframework.security.crypto.bcrypt.BCryptPasswordEncoder;

import javax.persistence.Entity;
import javax.persistence.Id;
import javax.persistence.Table;
import javax.validation.constraints.NotNull;
import java.time.OffsetDateTime;
import java.util.UUID;

@Entity
@Data
@Table(name = "users")
public class User {
  @Id
  @Type(type = "uuid-char")
  private UUID id;

  @NotNull
  private OffsetDateTime creationTime;

  private OffsetDateTime lastChangedTime;

  @NotNull
  private String username;

  @NotNull
  private String passwordHash;

  private String email;

  @NotNull
  private boolean enabled;

  public void setRawPassword(String rawPassword) {
    this.passwordHash = new BCryptPasswordEncoder().encode(rawPassword);
  }
}
