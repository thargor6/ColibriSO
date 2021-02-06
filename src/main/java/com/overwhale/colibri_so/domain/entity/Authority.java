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
@Table(name = "authorities")
public class Authority  {
  @Id
  @Type(type = "uuid-char")
  @NotNull
  private UUID id;

  @NotNull
  private String authority;

}
