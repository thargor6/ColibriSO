package com.overwhale.colibri_so.frontend.dto;

import com.fasterxml.jackson.annotation.JsonFormat;
import lombok.Data;

import javax.annotation.Nullable;
import javax.validation.constraints.NotNull;
import java.time.OffsetDateTime;
import java.util.UUID;

@Data
public class UserDto {
  @NotNull private UUID id;

  @JsonFormat(pattern = "yyyy-MM-dd'T'HH:mm:ss.SSSXXX")
  @Nullable
  private OffsetDateTime creationTime;

  @JsonFormat(pattern = "yyyy-MM-dd'T'HH:mm:ss.SSSXXX")
  @Nullable
  private OffsetDateTime lastChangedTime;

  @NotNull private String username;

  @NotNull private String passwordHash;

  @NotNull private boolean enabled;
}
