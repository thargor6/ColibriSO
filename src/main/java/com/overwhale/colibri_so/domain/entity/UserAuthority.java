package com.overwhale.colibri_so.domain.entity;

import lombok.Data;
import org.hibernate.annotations.Type;

import javax.persistence.Entity;
import javax.persistence.Id;
import javax.persistence.IdClass;
import javax.persistence.Table;
import javax.validation.constraints.NotNull;
import java.util.UUID;

@Entity
@Data
@Table(name = "user_authorities")
@IdClass(UserAuthorityKey.class)
public class UserAuthority {

  @NotNull
  @Id
  @Type(type = "uuid-char")
  private UUID userId;

  @NotNull
  @Id
  @Type(type = "uuid-char")
  private UUID authorityId;
}
