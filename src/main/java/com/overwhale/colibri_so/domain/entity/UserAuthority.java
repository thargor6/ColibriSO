package com.overwhale.colibri_so.domain.entity;

import lombok.Data;
import org.hibernate.annotations.Type;

import javax.persistence.*;
import javax.validation.constraints.NotNull;
import java.time.OffsetDateTime;
import java.util.UUID;

@Entity
@Data
@Table(name = "user_authorities")
@IdClass(UserAuthorityKey.class)
public class UserAuthority {

  @NotNull
  @Id
  @Column(insertable = false, updatable = false)
  @Type(type = "uuid-char")
  private UUID userId;

  @NotNull
  @ManyToOne
  @JoinColumn(name = "userId")
  private User user;

  @NotNull
  @Id
  @Column(insertable = false, updatable = false)
  @Type(type = "uuid-char")
  private UUID authorityId;

  @NotNull
  @ManyToOne
  @JoinColumn(name = "authorityId")
  private Authority authority;

}
