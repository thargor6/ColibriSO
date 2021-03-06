package com.overwhale.colibri_so.backend.entity;

import lombok.Data;
import org.hibernate.annotations.Type;

import javax.annotation.Nullable;
import javax.persistence.Entity;
import javax.persistence.Id;
import javax.persistence.Table;
import javax.validation.constraints.NotNull;
import java.time.OffsetDateTime;
import java.util.UUID;

@Entity
@Data
@Table(name = "user_details")
public class UserDetail {
  @NotNull
  @Id
  @Type(type = "uuid-char")
  private UUID userId;

  @NotNull private OffsetDateTime creationTime;

  @Nullable private OffsetDateTime lastChangedTime;

  @Nullable private String email;

  @Nullable private String fullName;

  @Nullable private String avatar;

  @Nullable private String avatarColor;

  @Nullable private String uiTheme;

  @NotNull private boolean asyncTableRefresh;
}
