package com.overwhale.colibri_so.frontend.dto;

import com.fasterxml.jackson.annotation.JsonFormat;
import lombok.Data;

import javax.annotation.Nullable;
import javax.validation.constraints.NotNull;
import java.time.OffsetDateTime;
import java.util.UUID;

@Data
public class UserDetailDto {
  @NotNull private UUID userId;

  @JsonFormat(pattern = "yyyy-MM-dd'T'HH:mm:ss.SSSXXX")
  @NotNull
  private OffsetDateTime creationTime;

  @JsonFormat(pattern = "yyyy-MM-dd'T'HH:mm:ss.SSSXXX")
  @Nullable
  private OffsetDateTime lastChangedTime;

  @Nullable private String email;

  @Nullable private String fullName;

  @Nullable private String avatar;

  @Nullable private String avatarColor;

  @Nullable private String uiTheme;
}
